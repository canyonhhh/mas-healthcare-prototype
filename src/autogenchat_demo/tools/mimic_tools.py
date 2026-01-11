from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, Iterable, List

import pandas as pd


def _coerce_hadm_ids(hadm_ids: Iterable[Any]) -> List[int]:
    cleaned: List[int] = []
    for value in hadm_ids:
        if value is None or (isinstance(value, float) and pd.isna(value)):
            continue
        try:
            cleaned.append(int(value))
        except (TypeError, ValueError):
            continue
    return cleaned


def _safe_to_datetime(series: pd.Series) -> pd.Series:
    return pd.to_datetime(series, errors="coerce")


def _table_summary(tables: Dict[str, pd.DataFrame]) -> Dict[str, Dict[str, Any]]:
    summary: Dict[str, Dict[str, Any]] = {}
    for name, df in tables.items():
        if not isinstance(df, pd.DataFrame):
            continue
        summary[name] = {"rows": int(df.shape[0]), "columns": list(df.columns)}
    return summary


def pick_cohort(dataset_dir: str, n: int, seed: int, strategy: str = "random") -> Dict[str, Any]:
    hosp_dir = Path(dataset_dir) / "hosp"
    admissions_path = hosp_dir / "admissions.csv"
    usecols = ["hadm_id", "subject_id", "admittime", "dischtime"]
    admissions = pd.read_csv(admissions_path, usecols=usecols)
    total_admissions = int(admissions.shape[0])
    if n >= total_admissions:
        cohort = admissions.copy()
    else:
        if strategy == "first_n":
            cohort = admissions.sort_values("hadm_id").head(n)
        elif strategy == "recent":
            if "admittime" in admissions.columns:
                cohort = admissions.sort_values("admittime", ascending=False).head(n)
            else:
                cohort = admissions.sort_values("hadm_id").head(n)
        else:
            cohort = admissions.sample(n=n, random_state=seed)

    hadm_ids = _coerce_hadm_ids(cohort["hadm_id"].tolist())
    cohort_preview = (
        cohort.sort_values("hadm_id").head(min(5, len(cohort))).to_dict(orient="records")
    )
    stats = {
        "total_admissions": total_admissions,
        "cohort_size": int(len(hadm_ids)),
        "seed": int(seed),
        "strategy": strategy,
    }
    return {
        "hadm_ids": hadm_ids,
        "cohort_preview": cohort_preview,
        "stats": stats,
    }


def load_hosp_tables(dataset_dir: str, hadm_ids: List[str | int]) -> Dict[str, Any]:
    hosp_dir = Path(dataset_dir) / "hosp"
    hadm_id_set = set(_coerce_hadm_ids(hadm_ids))

    admissions = pd.read_csv(hosp_dir / "admissions.csv")
    admissions = admissions[admissions["hadm_id"].isin(hadm_id_set)]

    subject_ids = set(_coerce_hadm_ids(admissions["subject_id"].tolist()))
    patients = pd.read_csv(hosp_dir / "patients.csv")
    if "subject_id" in patients.columns:
        patients = patients[patients["subject_id"].isin(subject_ids)]

    diagnoses_icd = pd.read_csv(hosp_dir / "diagnoses_icd.csv")
    if "hadm_id" in diagnoses_icd.columns:
        diagnoses_icd = diagnoses_icd[diagnoses_icd["hadm_id"].isin(hadm_id_set)]

    labevents_path = hosp_dir / "labevents.csv"
    lab_chunks: List[pd.DataFrame] = []
    for chunk in pd.read_csv(labevents_path, chunksize=100_000, low_memory=False):
        if "hadm_id" not in chunk.columns:
            continue
        filtered = chunk[chunk["hadm_id"].isin(hadm_id_set)]
        if not filtered.empty:
            lab_chunks.append(filtered)
    if lab_chunks:
        labevents = pd.concat(lab_chunks, ignore_index=True)
    else:
        labevents = pd.DataFrame(columns=["hadm_id"])

    d_icd_diagnoses = pd.read_csv(hosp_dir / "d_icd_diagnoses.csv")
    d_labitems = pd.read_csv(hosp_dir / "d_labitems.csv")

    tables: Dict[str, pd.DataFrame] = {
        "admissions": admissions,
        "patients": patients,
        "diagnoses_icd": diagnoses_icd,
        "labevents": labevents,
        "d_icd_diagnoses": d_icd_diagnoses,
        "d_labitems": d_labitems,
    }
    return {"tables": tables, "table_summary": _table_summary(tables)}


def normalize_hosp(tables: Dict[str, pd.DataFrame]) -> Dict[str, Any]:
    diagnoses = tables.get("diagnoses_icd", pd.DataFrame())
    icd_dict = tables.get("d_icd_diagnoses", pd.DataFrame())
    if not diagnoses.empty and not icd_dict.empty:
        diagnoses_norm = diagnoses.merge(
            icd_dict,
            on=["icd_code", "icd_version"],
            how="left",
            suffixes=("", "_dict"),
        )
    else:
        diagnoses_norm = diagnoses.copy()

    labevents = tables.get("labevents", pd.DataFrame())
    lab_dict = tables.get("d_labitems", pd.DataFrame())
    if not labevents.empty and not lab_dict.empty:
        labevents_norm = labevents.merge(
            lab_dict, on="itemid", how="left", suffixes=("", "_dict")
        )
    else:
        labevents_norm = labevents.copy()

    diag_mapped_col = "long_title" if "long_title" in diagnoses_norm.columns else None
    if diag_mapped_col:
        diag_coverage = float(diagnoses_norm[diag_mapped_col].notna().mean())
        unmapped_diag = diagnoses_norm[diagnoses_norm[diag_mapped_col].isna()]
        diag_top_unmapped = (
            unmapped_diag["icd_code"].value_counts().head(5).to_dict()
            if "icd_code" in unmapped_diag.columns
            else {}
        )
    else:
        diag_coverage = 0.0
        diag_top_unmapped = {}

    lab_mapped_col = "label" if "label" in labevents_norm.columns else None
    if lab_mapped_col:
        lab_coverage = float(labevents_norm[lab_mapped_col].notna().mean())
        unmapped_lab = labevents_norm[labevents_norm[lab_mapped_col].isna()]
        lab_top_unmapped = (
            unmapped_lab["itemid"].value_counts().head(5).to_dict()
            if "itemid" in unmapped_lab.columns
            else {}
        )
    else:
        lab_coverage = 0.0
        lab_top_unmapped = {}

    mapping_stats = {
        "icd_coverage": diag_coverage,
        "labitem_coverage": lab_coverage,
        "icd_top_unmapped": diag_top_unmapped,
        "labitem_top_unmapped": lab_top_unmapped,
    }

    tables_out = dict(tables)
    tables_out["diagnoses_norm"] = diagnoses_norm
    tables_out["labevents_norm"] = labevents_norm
    tables_out["mapping_stats"] = mapping_stats
    return {"tables": tables_out, "mapping_stats": mapping_stats}


def compute_features(tables: Dict[str, pd.DataFrame]) -> Dict[str, Any]:
    admissions = tables.get("admissions", pd.DataFrame())
    diagnoses = tables.get("diagnoses_norm", tables.get("diagnoses_icd", pd.DataFrame()))
    labevents = tables.get("labevents_norm", tables.get("labevents", pd.DataFrame()))

    features = pd.DataFrame()
    if not admissions.empty and "hadm_id" in admissions.columns:
        features["hadm_id"] = admissions["hadm_id"].astype("int64")
        if "admittime" in admissions.columns and "dischtime" in admissions.columns:
            admittime = _safe_to_datetime(admissions["admittime"])
            dischtime = _safe_to_datetime(admissions["dischtime"])
            los_hours = (dischtime - admittime).dt.total_seconds() / 3600
            features["length_of_stay_hours"] = los_hours
        else:
            features["length_of_stay_hours"] = pd.Series(
                [pd.NA] * len(features), index=features.index
            )

    diagnosis_counts = (
        diagnoses.groupby("hadm_id").size().rename("diagnosis_count")
        if not diagnoses.empty and "hadm_id" in diagnoses.columns
        else pd.Series(dtype="int64", name="diagnosis_count")
    )
    lab_counts = (
        labevents.groupby("hadm_id").size().rename("lab_count")
        if not labevents.empty and "hadm_id" in labevents.columns
        else pd.Series(dtype="int64", name="lab_count")
    )

    if "hadm_id" not in features.columns:
        features = pd.DataFrame({"hadm_id": pd.Series(dtype="int64")})
    features = features.merge(
        diagnosis_counts, left_on="hadm_id", right_index=True, how="left"
    )
    features = features.merge(
        lab_counts, left_on="hadm_id", right_index=True, how="left"
    )
    features["diagnosis_count"] = features["diagnosis_count"].fillna(0).astype(int)
    features["lab_count"] = features["lab_count"].fillna(0).astype(int)

    if "flag" in labevents.columns and "hadm_id" in labevents.columns:
        flag_present = labevents["flag"].notna() & (labevents["flag"].astype(str) != "")
        abnormal_counts = (
            labevents[flag_present].groupby("hadm_id").size().rename("abnormal_lab_count")
        )
        features = features.merge(
            abnormal_counts, left_on="hadm_id", right_index=True, how="left"
        )
        features["abnormal_lab_count"] = (
            features["abnormal_lab_count"].fillna(0).astype(int)
        )
        features["abnormal_fraction"] = features.apply(
            lambda row: row["abnormal_lab_count"] / row["lab_count"]
            if row["lab_count"] > 0
            else 0,
            axis=1,
        )

    features_summary = {
        "rows": int(features.shape[0]),
        "columns": list(features.columns),
    }
    preview = features.head(5).to_dict(orient="records")
    return {"features": features, "features_summary": features_summary, "preview": preview}


def run_safety_checks(
    tables: Dict[str, pd.DataFrame], features: Dict[str, Any]
) -> Dict[str, Any]:
    checks: List[Dict[str, Any]] = []

    admissions = tables.get("admissions", pd.DataFrame())
    labevents = tables.get("labevents_norm", tables.get("labevents", pd.DataFrame()))

    if (
        labevents.empty
        or "charttime" not in labevents.columns
        or admissions.empty
        or not {"hadm_id", "admittime", "dischtime"}.issubset(admissions.columns)
    ):
        checks.append(
            {
                "name": "temporal_window",
                "status": "warn",
                "details": "missing labevents or time columns",
            }
        )
    else:
        merged = labevents.merge(
            admissions[["hadm_id", "admittime", "dischtime"]],
            on="hadm_id",
            how="left",
        )
        charttime = _safe_to_datetime(merged["charttime"])
        admittime = _safe_to_datetime(merged["admittime"])
        dischtime = _safe_to_datetime(merged["dischtime"])
        in_window = charttime.between(admittime, dischtime)
        out_of_window = int((~in_window.fillna(False)).sum())
        status = "pass" if out_of_window == 0 else "warn"
        checks.append(
            {
                "name": "temporal_window",
                "status": status,
                "details": {"out_of_window_count": out_of_window},
            }
        )

    key_nulls: Dict[str, int] = {}
    critical_tables = {
        "admissions": ("hadm_id", "subject_id"),
        "patients": ("subject_id",),
        "diagnoses": ("hadm_id", "subject_id"),
        "labevents": ("hadm_id", "subject_id"),
    }
    table_map = {
        "admissions": admissions,
        "patients": tables.get("patients", pd.DataFrame()),
        "diagnoses": tables.get("diagnoses_norm", tables.get("diagnoses_icd", pd.DataFrame())),
        "labevents": labevents,
    }
    for table_name, columns in critical_tables.items():
        df = table_map.get(table_name, pd.DataFrame())
        for column in columns:
            if column in df.columns:
                key_nulls[f"{table_name}.{column}"] = int(df[column].isna().sum())

    any_nulls = any(count > 0 for count in key_nulls.values())
    checks.append(
        {
            "name": "key_integrity",
            "status": "fail" if any_nulls else "pass",
            "details": key_nulls,
        }
    )

    mapping_stats = tables.get("mapping_stats", {})
    icd_cov = float(mapping_stats.get("icd_coverage", 0.0)) if mapping_stats else 0.0
    lab_cov = float(mapping_stats.get("labitem_coverage", 0.0)) if mapping_stats else 0.0
    status = (
        "pass"
        if icd_cov >= 0.9 and lab_cov >= 0.9
        else "warn"
    )
    checks.append(
        {
            "name": "mapping_coverage",
            "status": status,
            "details": {"icd_coverage": icd_cov, "labitem_coverage": lab_cov},
        }
    )

    missingness: Dict[str, float] = {}
    missing_fields = {
        "admissions": ("admittime", "dischtime", "subject_id", "hadm_id"),
        "diagnoses": ("icd_code", "icd_version", "hadm_id"),
        "labevents": ("itemid", "charttime", "hadm_id"),
    }
    for table_name, columns in missing_fields.items():
        df = table_map.get(table_name, pd.DataFrame())
        if df.empty:
            continue
        for column in columns:
            if column in df.columns:
                missingness[f"{table_name}.{column}"] = float(
                    df[column].isna().mean()
                )

    missing_threshold = 0.1
    missing_over = {k: v for k, v in missingness.items() if v > missing_threshold}
    checks.append(
        {
            "name": "missingness",
            "status": "warn" if missing_over else "pass",
            "details": missingness,
        }
    )

    summary = {
        "pass": sum(1 for check in checks if check["status"] == "pass"),
        "warn": sum(1 for check in checks if check["status"] == "warn"),
        "fail": sum(1 for check in checks if check["status"] == "fail"),
    }
    return {"checks": checks, "summary": summary}


def _markdown_table(rows: List[Dict[str, Any]]) -> str:
    if not rows:
        return "_No data_"
    headers = list(rows[0].keys())
    header_row = "| " + " | ".join(headers) + " |"
    sep_row = "| " + " | ".join(["---"] * len(headers)) + " |"
    body_rows = []
    for row in rows:
        body_rows.append("| " + " | ".join(str(row.get(h, "")) for h in headers) + " |")
    return "\n".join([header_row, sep_row] + body_rows)


def write_report(
    run_dir: str,
    cohort: Dict[str, Any],
    table_summary: Dict[str, Any],
    features: Dict[str, Any],
    checks: Dict[str, Any],
    audit_log: List[Dict[str, Any]],
) -> Dict[str, Any]:
    run_path = Path(run_dir)
    run_path.mkdir(parents=True, exist_ok=True)

    features_df = features.get("features", pd.DataFrame())
    features_preview = features.get("preview", [])
    report_payload = {
        "generated_at": datetime.utcnow().isoformat(),
        "cohort": cohort,
        "table_summary": table_summary,
        "features": features_df.to_dict(orient="records"),
        "features_summary": features.get("features_summary", {}),
        "checks": checks,
    }

    report_json_path = run_path / "cohort_report.json"
    with report_json_path.open("w", encoding="utf-8") as handle:
        json.dump(report_payload, handle, indent=2, default=str)

    report_md_path = run_path / "cohort_report.md"
    validation_summary = checks.get("summary", {})
    md_lines = [
        "# Cohort Report",
        "",
        f"Generated: {report_payload['generated_at']}",
        "",
        "## Cohort",
        f"Cohort size: {cohort.get('stats', {}).get('cohort_size', 0)}",
        "",
        "## Table Row Counts",
    ]
    for table, summary in table_summary.items():
        md_lines.append(f"- {table}: {summary.get('rows', 0)} rows")

    md_lines.extend(
        [
            "",
            "## Feature Preview (Top 5)",
            _markdown_table(features_preview),
            "",
            "## Validation Checklist",
            f"- Pass: {validation_summary.get('pass', 0)}",
            f"- Warn: {validation_summary.get('warn', 0)}",
            f"- Fail: {validation_summary.get('fail', 0)}",
        ]
    )

    with report_md_path.open("w", encoding="utf-8") as handle:
        handle.write("\n".join(md_lines))

    audit_log_path = run_path / "audit_log.jsonl"
    with audit_log_path.open("w", encoding="utf-8") as handle:
        for entry in audit_log:
            handle.write(json.dumps(entry, default=str) + "\n")

    return {
        "run_dir": str(run_path),
        "files": {
            "cohort_report_json": str(report_json_path),
            "cohort_report_md": str(report_md_path),
            "audit_log": str(audit_log_path),
        },
    }

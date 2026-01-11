from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Tuple

import pandas as pd

from .config import get_config
from .contracts import AgentResult, ArtifactSpec, CheckResult, PipelinePaths
from .io import (
    DATA_ROOT,
    load_admissions,
    load_diagnoses,
    load_icd_map,
    load_labitems_map,
    load_labevents,
    load_patients,
)
from .registry import append_audit, register_artifact

ArtifactName = str


def _write_csv(df: pd.DataFrame, path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(path, index=False)


def _artifact(path: Path, name: ArtifactName, df: pd.DataFrame, lineage: List[str]) -> ArtifactSpec:
    return ArtifactSpec(
        name=name,
        path=str(path),
        rows=int(len(df)),
        schema=[str(c) for c in df.columns],
        lineage=lineage,
    )


def _add_check(checks: List[CheckResult], name: str, status: str, details: str, metrics: Dict) -> None:
    checks.append(CheckResult(name=name, status=status, details=details, metrics=metrics))


def ingest(paths: PipelinePaths | None = None, data_root: Path | None = None) -> AgentResult:
    paths = paths or PipelinePaths.default(Path("."))
    data_root = data_root or DATA_ROOT

    patients = load_patients(data_root)
    admissions = load_admissions(data_root)
    diagnoses = load_diagnoses(data_root)
    labs = load_labevents(data_root)

    # Build base admissions table (one row per admission with patient info).
    admissions_base = admissions.merge(
        patients,
        on="subject_id",
        how="left",
        suffixes=("", "_patient"),
    )

    artifacts: List[ArtifactSpec] = []
    checks: List[CheckResult] = []
    metrics: Dict[str, float] = {
        "patients_rows": len(patients),
        "admissions_rows": len(admissions),
        "diagnoses_rows": len(diagnoses),
        "labs_rows": len(labs),
    }

    # Validations.
    _add_check(
        checks,
        "patients_subject_id_unique",
        "pass" if patients["subject_id"].is_unique else "fail",
        "Each subject_id should be unique in patients.",
        {"unique": int(patients["subject_id"].is_unique), "rows": len(patients)},
    )
    _add_check(
        checks,
        "admissions_hadm_id_unique",
        "pass" if admissions["hadm_id"].is_unique else "fail",
        "Each hadm_id should be unique in admissions.",
        {"unique": int(admissions["hadm_id"].is_unique), "rows": len(admissions)},
    )

    missing_diag_keys = diagnoses["hadm_id"].isna().sum()
    missing_lab_keys = labs["hadm_id"].isna().sum()
    orphan_diag = diagnoses["hadm_id"].isin(admissions["hadm_id"]).mean() < 1.0
    orphan_lab = labs["hadm_id"].isin(admissions["hadm_id"]).mean() < 1.0
    _add_check(
        checks,
        "missing_keys",
        "warn" if (missing_diag_keys + missing_lab_keys) > 0 else "pass",
        "Missing hadm_id in diagnoses or labs.",
        {"missing_diagnoses": int(missing_diag_keys), "missing_labs": int(missing_lab_keys)},
    )
    _add_check(
        checks,
        "orphan_records",
        "warn" if (orphan_diag or orphan_lab) else "pass",
        "Records pointing to unknown hadm_id.",
        {
            "diagnoses_orphan_fraction": float(1 - diagnoses["hadm_id"].isin(admissions["hadm_id"]).mean()),
            "labs_orphan_fraction": float(1 - labs["hadm_id"].isin(admissions["hadm_id"]).mean()),
        },
    )

    # Persist artifacts.
    admissions_base_path = paths.artifacts_dir / "admissions_base.csv"
    diagnoses_path = paths.artifacts_dir / "admission_diagnoses.csv"
    labs_path = paths.artifacts_dir / "admission_labs.csv"

    _write_csv(admissions_base, admissions_base_path)
    _write_csv(diagnoses, diagnoses_path)
    _write_csv(labs, labs_path)

    artifacts.append(_artifact(admissions_base_path, "admissions_base", admissions_base, ["patients", "admissions"]))
    artifacts.append(_artifact(diagnoses_path, "admission_diagnoses", diagnoses, ["diagnoses_icd"]))
    artifacts.append(_artifact(labs_path, "admission_labs", labs, ["labevents"]))

    result = AgentResult(
        agent="ingestion",
        artifacts=artifacts,
        checks=checks,
        metrics=metrics,
        notes="Loaded source CSVs and wrote normalized admissions/diagnoses/labs tables.",
    )
    append_audit(paths, result)
    for art in artifacts:
        register_artifact(paths, art)
    return result


def normalize(paths: PipelinePaths | None = None, data_root: Path | None = None) -> AgentResult:
    paths = paths or PipelinePaths.default(Path("."))
    data_root = data_root or DATA_ROOT

    diagnoses = pd.read_csv(paths.artifacts_dir / "admission_diagnoses.csv")
    labs = pd.read_csv(paths.artifacts_dir / "admission_labs.csv", parse_dates=["charttime", "storetime"])

    icd_map = load_icd_map(data_root)
    labitems = load_labitems_map(data_root)

    diag_norm = diagnoses.merge(
        icd_map,
        on=["icd_code", "icd_version"],
        how="left",
    )
    diag_norm["diagnosis_name"] = diag_norm["long_title"]
    diag_norm["mapped"] = diag_norm["diagnosis_name"].notna()

    labs_norm = labs.merge(labitems, on="itemid", how="left")
    labs_norm["lab_label"] = labs_norm["label"]
    labs_norm["mapped"] = labs_norm["lab_label"].notna()

    # Unit consistency per itemid.
    unit_counts = labs_norm.groupby("itemid")["valueuom"].nunique(dropna=True)
    inconsistent_items = set(unit_counts[unit_counts > 1].index.tolist())
    labs_norm["unit_status"] = "ok"
    labs_norm.loc[labs_norm["valueuom"].isna(), "unit_status"] = "unknown"
    labs_norm.loc[labs_norm["itemid"].isin(inconsistent_items), "unit_status"] = "inconsistent"

    # Metrics and checks.
    artifacts: List[ArtifactSpec] = []
    checks: List[CheckResult] = []
    metrics: Dict[str, float] = {
        "diagnoses_total": len(diag_norm),
        "diagnoses_mapped": float(diag_norm["mapped"].mean()) if len(diag_norm) else 0.0,
        "labs_total": len(labs_norm),
        "labs_mapped": float(labs_norm["mapped"].mean()) if len(labs_norm) else 0.0,
        "lab_items_inconsistent_units": len(inconsistent_items),
    }

    _add_check(
        checks,
        "diagnosis_mapping",
        "warn" if diag_norm["mapped"].mean() < 1.0 else "pass",
        "Mapped ICD codes to long titles; unmapped remain flagged.",
        {"mapped_fraction": float(diag_norm["mapped"].mean()) if len(diag_norm) else 0.0},
    )
    _add_check(
        checks,
        "labitem_mapping",
        "warn" if labs_norm["mapped"].mean() < 1.0 else "pass",
        "Mapped lab itemids to labels; unmapped remain flagged.",
        {"mapped_fraction": float(labs_norm["mapped"].mean()) if len(labs_norm) else 0.0},
    )
    _add_check(
        checks,
        "unit_consistency",
        "warn" if inconsistent_items else "pass",
        "Value units should be consistent per itemid.",
        {"inconsistent_itemids": list(map(int, inconsistent_items))},
    )

    diag_norm_path = paths.artifacts_dir / "diagnoses_normalized.csv"
    labs_norm_path = paths.artifacts_dir / "labs_normalized.csv"
    _write_csv(diag_norm, diag_norm_path)
    _write_csv(labs_norm, labs_norm_path)

    artifacts.append(_artifact(diag_norm_path, "diagnoses_normalized", diag_norm, ["admission_diagnoses", "d_icd_diagnoses"]))
    artifacts.append(_artifact(labs_norm_path, "labs_normalized", labs_norm, ["admission_labs", "d_labitems"]))

    result = AgentResult(
        agent="normalization",
        artifacts=artifacts,
        checks=checks,
        metrics=metrics,
        notes="Normalized diagnoses and labs with mapping and unit status.",
    )
    append_audit(paths, result)
    for art in artifacts:
        register_artifact(paths, art)
    return result


def _abnormal_mask(df: pd.DataFrame) -> pd.Series:
    flag_mask = df["flag"].fillna("").str.lower() == "abnormal"
    has_range = df["valuenum"].notna() & df["ref_range_lower"].notna() & df["ref_range_upper"].notna()
    range_mask = has_range & (
        (df["valuenum"] < df["ref_range_lower"]) | (df["valuenum"] > df["ref_range_upper"])
    )
    return flag_mask | range_mask


def analyze(paths: PipelinePaths | None = None) -> AgentResult:
    paths = paths or PipelinePaths.default(Path("."))
    cfg = get_config(paths.artifacts_dir / "config_override.json")

    admissions = pd.read_csv(
        paths.artifacts_dir / "admissions_base.csv",
        parse_dates=["admittime", "dischtime", "deathtime", "edregtime", "edouttime", "dod"],
    )
    diag_norm = pd.read_csv(paths.artifacts_dir / "diagnoses_normalized.csv")
    labs_norm = pd.read_csv(paths.artifacts_dir / "labs_normalized.csv", parse_dates=["charttime", "storetime"])

    # Features.
    num_diag = diag_norm.groupby("hadm_id").size().rename("num_diagnoses")
    labs_norm["is_abnormal"] = _abnormal_mask(labs_norm)
    num_abn = labs_norm.groupby("hadm_id")["is_abnormal"].sum().rename("num_abnormal_labs")

    features = admissions[["hadm_id", "subject_id", "admittime", "dischtime"]].copy()
    features["length_of_stay_hours"] = (
        (features["dischtime"] - features["admittime"]).dt.total_seconds() / 3600.0
    )
    features = features.merge(num_diag, on="hadm_id", how="left").merge(num_abn, on="hadm_id", how="left")
    features["num_diagnoses"] = features["num_diagnoses"].fillna(0).astype(int)
    features["num_abnormal_labs"] = features["num_abnormal_labs"].fillna(0).astype(int)
    features["length_of_stay_hours"] = features["length_of_stay_hours"].fillna(0).clip(lower=0)

    rr = cfg["risk_rule"]
    features["risk_flag"] = (
        (features["length_of_stay_hours"] > rr["los_hours_high"])
        | (features["num_abnormal_labs"] > rr["abnormal_lab_threshold"])
        | (features["num_diagnoses"] > rr["diagnosis_threshold"])
    ).astype(int)

    artifacts: List[ArtifactSpec] = []
    checks: List[CheckResult] = []
    metrics: Dict[str, float] = {
        "hadm_count": len(features),
        "risk_flag_rate": float(features["risk_flag"].mean()) if len(features) else 0.0,
    }

    # Validations.
    negative_los = (features["length_of_stay_hours"] < 0).sum()
    missing_any = features[["hadm_id", "length_of_stay_hours", "num_diagnoses", "num_abnormal_labs"]].isna().any(axis=1).sum()
    _add_check(
        checks,
        "los_non_negative",
        "fail" if negative_los else "pass",
        "Length of stay should be non-negative.",
        {"negative_rows": int(negative_los)},
    )
    _add_check(
        checks,
        "features_non_missing",
        "fail" if missing_any else "pass",
        "Critical features should not be missing.",
        {"rows_with_missing": int(missing_any)},
    )

    feat_path = paths.artifacts_dir / "features_by_admission.csv"
    _write_csv(features, feat_path)
    artifacts.append(_artifact(feat_path, "features_by_admission", features, ["admissions_base", "diagnoses_normalized", "labs_normalized"]))

    result = AgentResult(
        agent="analysis",
        artifacts=artifacts,
        checks=checks,
        metrics=metrics,
        notes="Computed counts, LOS, and a simple rule-based risk flag.",
    )
    append_audit(paths, result)
    for art in artifacts:
        register_artifact(paths, art)
    return result


def safety(paths: PipelinePaths | None = None) -> AgentResult:
    paths = paths or PipelinePaths.default(Path("."))
    cfg_all = get_config(paths.artifacts_dir / "config_override.json")
    cfg = cfg_all["safety_rules"]

    admissions = pd.read_csv(
        paths.artifacts_dir / "admissions_base.csv",
        parse_dates=["admittime", "dischtime", "deathtime", "edregtime", "edouttime", "dod"],
    )
    labs_norm = pd.read_csv(paths.artifacts_dir / "labs_normalized.csv", parse_dates=["charttime", "storetime"])
    diag_norm = pd.read_csv(paths.artifacts_dir / "diagnoses_normalized.csv")

    artifacts: List[ArtifactSpec] = []
    checks: List[CheckResult] = []
    metrics: Dict[str, float] = {}
    stop = False

    # Leakage: labs after discharge.
    labs_join = labs_norm.merge(admissions[["hadm_id", "dischtime"]], on="hadm_id", how="left")
    future_labs = labs_join[labs_join["dischtime"].notna() & (labs_join["charttime"] > labs_join["dischtime"])]
    leakage_count = len(future_labs)
    leakage_status = "fail" if (cfg["fail_on_future_labs"] and leakage_count > 0) else ("warn" if leakage_count else "pass")
    _add_check(
        checks,
        "no_future_labs",
        leakage_status,
        "Lab charttime should not exceed discharge time.",
        {"future_labs": int(leakage_count)},
    )
    if leakage_status == "fail":
        stop = True

    # Plausible lab ranges.
    ranges = cfg["plausible_lab_ranges"]
    labs_norm["lab_label_lower"] = labs_norm["lab_label"].str.lower()
    out_of_range_rows = []
    for label_lower, bounds in ranges.items():
        low, high = bounds
        mask = labs_norm["lab_label_lower"] == label_lower
        candidates = labs_norm[mask & labs_norm["valuenum"].notna()]
        bad = candidates[(candidates["valuenum"] < low) | (candidates["valuenum"] > high)]
        if len(bad):
            out_of_range_rows.append(bad)
    out_of_range = pd.concat(out_of_range_rows) if out_of_range_rows else pd.DataFrame(columns=labs_norm.columns)
    _add_check(
        checks,
        "plausible_ranges",
        "warn" if len(out_of_range) else "pass",
        "Lab values outside plausible bounds are flagged.",
        {"out_of_range_count": int(len(out_of_range))},
    )

    # dx↔lab coherence (warning-level).
    diag_norm["diagnosis_name_lower"] = diag_norm["diagnosis_name"].fillna("").str.lower()
    labs_norm["lab_label_lower"] = labs_norm["lab_label_lower"].fillna("")
    pair_warnings = 0
    for pair in cfg["dx_lab_pairs"]:
        dx_term = pair["diagnosis_contains"]
        lab_term = pair["lab_label_contains"]
        hadms_with_dx = set(
            diag_norm[diag_norm["diagnosis_name_lower"].str.contains(dx_term, na=False)]["hadm_id"].tolist()
        )
        hadms_with_lab = set(
            labs_norm[labs_norm["lab_label_lower"].str.contains(lab_term, na=False)]["hadm_id"].tolist()
        )
        missing_lab_for_dx = hadms_with_dx - hadms_with_lab
        if missing_lab_for_dx:
            pair_warnings += len(missing_lab_for_dx)
            _add_check(
                checks,
                f"dx_lab_coherence_{dx_term}_{lab_term}",
                "warn",
                f"Admissions with diagnosis containing '{dx_term}' missing labs containing '{lab_term}'.",
                {"hadm_ids": sorted(map(int, missing_lab_for_dx))},
            )

    # Missingness threshold for labs.
    admissions_with_labs = labs_norm["hadm_id"].dropna().nunique()
    total_adm = admissions["hadm_id"].nunique()
    labs_missing_fraction = 1 - (admissions_with_labs / total_adm if total_adm else 0)
    miss_status = "pass"
    if labs_missing_fraction >= cfg["labs_missing_fail"]:
        miss_status = "fail"
    elif labs_missing_fraction >= cfg["labs_missing_warn"]:
        miss_status = "warn"
    _add_check(
        checks,
        "lab_missingness",
        miss_status,
        "Fraction of admissions without any labs.",
        {"missing_fraction": float(labs_missing_fraction)},
    )
    if miss_status == "fail":
        stop = True

    metrics.update(
        {
            "future_labs": int(leakage_count),
            "out_of_range_labs": int(len(out_of_range)),
            "labs_missing_fraction": float(labs_missing_fraction),
        }
    )

    safety_report = {
        "status": "fail" if stop else "pass",
        "checks": [c.to_dict() for c in checks],
        "metrics": metrics,
        "generated_at": datetime.utcnow().isoformat() + "Z",
    }
    report_path = paths.artifacts_dir / "safety_report.json"
    report_path.write_text(json.dumps(safety_report, indent=2), encoding="utf-8")
    artifacts: List[ArtifactSpec] = [
        _artifact(report_path, "safety_report", pd.DataFrame([safety_report]), ["features_by_admission", "labs_normalized", "diagnoses_normalized"])
    ]

    result = AgentResult(
        agent="safety",
        artifacts=artifacts,
        checks=checks,
        metrics=metrics,
        notes="Safety checks for leakage, plausible ranges, dx-lab coherence, and lab missingness.",
        stop=stop,
    )
    append_audit(paths, result)
    for art in artifacts:
        register_artifact(paths, art)
    return result


def report(paths: PipelinePaths | None = None) -> AgentResult:
    paths = paths or PipelinePaths.default(Path("."))

    features = pd.read_csv(paths.artifacts_dir / "features_by_admission.csv")
    admissions = pd.read_csv(paths.artifacts_dir / "admissions_base.csv")
    diag_norm = pd.read_csv(paths.artifacts_dir / "diagnoses_normalized.csv")
    labs_norm = pd.read_csv(paths.artifacts_dir / "labs_normalized.csv")
    safety_report = json.loads((paths.artifacts_dir / "safety_report.json").read_text(encoding="utf-8"))
    audit_log = paths.audit_log_path.read_text(encoding="utf-8").splitlines()

    # Cohort description.
    cohort_lines = [
        f"- Admissions: {len(admissions):,}",
        f"- Patients: {admissions['subject_id'].nunique():,}",
        f"- Admissions with labs: {labs_norm['hadm_id'].dropna().nunique():,}",
    ]

    # Feature summary.
    feat_summary = []
    for col in ["length_of_stay_hours", "num_diagnoses", "num_abnormal_labs", "risk_flag"]:
        if col in features:
            feat_summary.append(
                f"- {col}: min {features[col].min():.2f}, max {features[col].max():.2f}, mean {features[col].mean():.2f}"
            )

    risk_rate = features["risk_flag"].mean() if "risk_flag" in features else 0

    report_md = "\n".join(
        [
            "# MAS Healthcare Prototype Report",
            "## Cohort",
            *cohort_lines,
            "",
            "## Features",
            *feat_summary,
            "",
            "## Risk Summary",
            f"- Risk flag rate: {risk_rate:.2%}",
            "",
            "## Safety",
            f"- Safety status: {safety_report.get('status','unknown')}",
            f"- Checks: {len(safety_report.get('checks', []))} recorded",
        ]
    )
    report_path = paths.artifacts_dir / "report.md"
    report_path.write_text(report_md, encoding="utf-8")

    audit_md_lines = ["# Audit Log"]
    for line in audit_log:
        audit_md_lines.append(f"- {line}")
    audit_md = "\n".join(audit_md_lines)
    audit_summary_path = paths.artifacts_dir / "audit_summary.md"
    audit_summary_path.write_text(audit_md, encoding="utf-8")

    artifacts: List[ArtifactSpec] = [
        _artifact(report_path, "report_md", pd.DataFrame(), ["features_by_admission", "safety_report"]),
        _artifact(audit_summary_path, "audit_summary_md", pd.DataFrame(), []),
    ]

    result = AgentResult(
        agent="reporting",
        artifacts=artifacts,
        checks=[],
        metrics={"risk_flag_rate": float(risk_rate)},
        notes="Generated cohort/feature/risk summaries and audit log extracts.",
        stop=True,
    )
    append_audit(paths, result)
    for art in artifacts:
        register_artifact(paths, art)
    return result

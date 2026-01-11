from __future__ import annotations

from pathlib import Path
from typing import Optional

import pandas as pd


DATA_ROOT = Path("dataset/hosp")


def _csv_path(filename: str, data_root: Path | None = None) -> Path:
    root = data_root or DATA_ROOT
    return root / filename


def load_patients(data_root: Path | None = None) -> pd.DataFrame:
    path = _csv_path("patients.csv", data_root)
    return pd.read_csv(
        path,
        dtype={
            "subject_id": "Int64",
            "gender": "string",
            "anchor_age": "Int64",
            "anchor_year": "Int64",
            "anchor_year_group": "string",
            "dod": "string",
        },
        parse_dates=["dod"],
    )


def load_admissions(data_root: Path | None = None) -> pd.DataFrame:
    path = _csv_path("admissions.csv", data_root)
    return pd.read_csv(
        path,
        dtype={
            "subject_id": "Int64",
            "hadm_id": "Int64",
            "admission_type": "string",
            "admit_provider_id": "string",
            "admission_location": "string",
            "discharge_location": "string",
            "insurance": "string",
            "language": "string",
            "marital_status": "string",
            "race": "string",
            "hospital_expire_flag": "Int64",
        },
        parse_dates=[
            "admittime",
            "dischtime",
            "deathtime",
            "edregtime",
            "edouttime",
        ],
    )


def load_diagnoses(data_root: Path | None = None) -> pd.DataFrame:
    path = _csv_path("diagnoses_icd.csv", data_root)
    return pd.read_csv(
        path,
        dtype={
            "subject_id": "Int64",
            "hadm_id": "Int64",
            "seq_num": "Int64",
            "icd_code": "string",
            "icd_version": "Int64",
        },
    )


def load_icd_map(data_root: Path | None = None) -> pd.DataFrame:
    path = _csv_path("d_icd_diagnoses.csv", data_root)
    return pd.read_csv(
        path,
        dtype={
            "icd_code": "string",
            "icd_version": "Int64",
            "long_title": "string",
        },
    )


def load_labevents(data_root: Path | None = None) -> pd.DataFrame:
    path = _csv_path("labevents.csv", data_root)
    return pd.read_csv(
        path,
        dtype={
            "labevent_id": "Int64",
            "subject_id": "Int64",
            "hadm_id": "Int64",
            "specimen_id": "Int64",
            "itemid": "Int64",
            "order_provider_id": "string",
            "value": "string",
            "valuenum": "float",
            "valueuom": "string",
            "ref_range_lower": "float",
            "ref_range_upper": "float",
            "flag": "string",
            "priority": "string",
            "comments": "string",
        },
        parse_dates=["charttime", "storetime"],
    )


def load_labitems_map(data_root: Path | None = None) -> pd.DataFrame:
    path = _csv_path("d_labitems.csv", data_root)
    return pd.read_csv(
        path,
        dtype={
            "itemid": "Int64",
            "label": "string",
            "fluid": "string",
            "category": "string",
        },
    )

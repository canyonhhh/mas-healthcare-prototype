from __future__ import annotations

from copy import deepcopy
from typing import Any, Dict

# Thresholds for the simple rule-based risk flag.
RISK_RULE: Dict[str, Any] = {
    "los_hours_high": 72,  # 3 days
    "abnormal_lab_threshold": 2,
    "diagnosis_threshold": 5,
}

# Safety thresholds and plausible ranges.
SAFETY_RULES: Dict[str, Any] = {
    # If a lab occurs after discharge, mark as leakage (default warn-only).
    "fail_on_future_labs": False,
    # Fraction of admissions without any labs that triggers warnings/failures.
    "labs_missing_warn": 0.3,
    "labs_missing_fail": 0.6,
    # Plausible ranges keyed by lab label (case-insensitive match).
    "plausible_lab_ranges": {
        "glucose": (40, 500),
        "sodium": (110, 170),
        "potassium": (2, 8),
        "creatinine": (0.1, 20),
        "hemoglobin": (5, 20),
        "hematocrit": (15, 70),
        "wbc": (0.5, 50),
        "platelet count": (5, 1500),
        "lactate": (0.2, 20),
    },
    # Light-touch dx↔lab coherence checks (warning-level).
    "dx_lab_pairs": [
        {"diagnosis_contains": "diabetes", "lab_label_contains": "glucose"},
        {"diagnosis_contains": "renal", "lab_label_contains": "creatinine"},
    ],
}

# Default config merged for all steps.
DEFAULT_CONFIG: Dict[str, Any] = {
    "risk_rule": RISK_RULE,
    "safety_rules": SAFETY_RULES,
}


def _deep_update(base: Dict[str, Any], override: Dict[str, Any]) -> Dict[str, Any]:
    for k, v in override.items():
        if isinstance(v, dict) and isinstance(base.get(k), dict):
            base[k] = _deep_update(base[k], v)
        else:
            base[k] = v
    return base


def get_config(override_path: str | None = None) -> Dict[str, Any]:
    """
    Return a deep copy of config. If override_path is provided and exists,
    merge that JSON (user goal overrides) into the defaults.
    """
    cfg = deepcopy(DEFAULT_CONFIG)
    if override_path:
        from pathlib import Path
        path = Path(override_path)
        if path.exists():
            import json
            override = json.loads(path.read_text(encoding="utf-8") or "{}")
            cfg = _deep_update(cfg, override)
    return cfg

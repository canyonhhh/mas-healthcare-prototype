from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any, Dict


def parse_goal_to_config(goal: str, base_config: Dict[str, Any]) -> Dict[str, Any]:
    """
    Parse a natural language goal string and return an override config dict.
    Supported tweaks:
    - Thresholds: LOS hours, abnormal labs, diagnosis count.
    - Future labs: "warn on future labs" / "fail on future labs".
    """
    text = goal.lower()
    overrides: Dict[str, Any] = {}

    def set_path(path: str, value: Any) -> None:
        parts = path.split(".")
        cur = overrides
        for p in parts[:-1]:
            cur = cur.setdefault(p, {})
        cur[parts[-1]] = value

    # Future labs policy.
    if "fail future lab" in text or "fail on future lab" in text:
        set_path("safety_rules.fail_on_future_labs", True)
    elif "warn future lab" in text or "warn on future lab" in text or "ignore future lab" in text:
        set_path("safety_rules.fail_on_future_labs", False)

    # Threshold helpers.
    def extract_number_after(keyword: str) -> int | None:
        m = re.search(rf"{keyword}[^0-9]{{0,10}}([0-9]+)", text)
        if m:
            return int(m.group(1))
        return None

    los_hours = extract_number_after("los") or extract_number_after("length of stay")
    if los_hours is None:
        m = re.search(r"([0-9]+)\s*day", text)
        if m:
            los_hours = int(m.group(1)) * 24
    if los_hours is not None:
        set_path("risk_rule.los_hours_high", los_hours)

    abn = extract_number_after("abnormal lab")
    if abn is not None:
        set_path("risk_rule.abnormal_lab_threshold", abn)

    dx = extract_number_after("diagnosis") or extract_number_after("diagnoses")
    if dx is not None:
        set_path("risk_rule.diagnosis_threshold", dx)

    # Merge overrides into base_config copy.
    merged = json.loads(json.dumps(base_config))  # deep copy
    for path, value in _flatten(overrides).items():
        parts = path.split(".")
        cur = merged
        for p in parts[:-1]:
            cur = cur.setdefault(p, {})
        cur[parts[-1]] = value
    return merged


def _flatten(d: Dict[str, Any], prefix: str = "") -> Dict[str, Any]:
    flat = {}
    for k, v in d.items():
        key = f"{prefix}.{k}" if prefix else k
        if isinstance(v, dict):
            flat.update(_flatten(v, key))
        else:
            flat[key] = v
    return flat


def write_override(goal: str, base_config: Dict[str, Any], override_path: Path) -> Dict[str, Any]:
    merged = parse_goal_to_config(goal, base_config)
    override_path.parent.mkdir(parents=True, exist_ok=True)
    override_path.write_text(json.dumps(merged, indent=2), encoding="utf-8")
    return merged

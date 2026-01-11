from __future__ import annotations

from typing import Any, Dict, List, Tuple

PLAN_VERSION = 1
ALLOWED_PIPELINES = {"cohort_report"}
ALLOWED_STRATEGIES = {"random", "first_n", "recent"}
ALLOWED_OUTPUT_FORMATS = {"md", "json", "both"}


def default_plan() -> Dict[str, Any]:
    return {
        "plan_version": PLAN_VERSION,
        "pipeline": "cohort_report",
        "cohort": {"n": 5, "seed": 1, "strategy": "random"},
        "steps": {
            "ingestion": True,
            "normalization": True,
            "analysis": True,
            "safety": True,
            "reporting": True,
        },
        "output": {"format": "both"},
        "notes": "",
    }


def _unknown_keys(data: Dict[str, Any], allowed: set[str]) -> List[str]:
    return sorted(set(data.keys()) - allowed)


def validate_plan(plan: Dict[str, Any]) -> Tuple[Dict[str, Any], List[str]]:
    errors: List[str] = []
    validated = default_plan()

    if not isinstance(plan, dict):
        return validated, ["plan must be a dict"]

    top_allowed = {"plan_version", "pipeline", "cohort", "steps", "output", "notes"}
    top_unknown = _unknown_keys(plan, top_allowed)
    if top_unknown:
        errors.append(f"unknown top-level keys: {top_unknown}")

    plan_version = plan.get("plan_version")
    if isinstance(plan_version, int):
        validated["plan_version"] = plan_version
    else:
        errors.append("plan_version must be int")

    pipeline = plan.get("pipeline")
    if pipeline in ALLOWED_PIPELINES:
        validated["pipeline"] = pipeline
    else:
        errors.append(f"pipeline must be one of {sorted(ALLOWED_PIPELINES)}")

    cohort = plan.get("cohort")
    if isinstance(cohort, dict):
        cohort_unknown = _unknown_keys(cohort, {"n", "seed", "strategy"})
        if cohort_unknown:
            errors.append(f"unknown cohort keys: {cohort_unknown}")
        n = cohort.get("n")
        if isinstance(n, int) and 1 <= n <= 50:
            validated["cohort"]["n"] = n
        else:
            errors.append("cohort.n must be int in range 1..50")
        seed = cohort.get("seed")
        if isinstance(seed, int) and seed >= 0:
            validated["cohort"]["seed"] = seed
        else:
            errors.append("cohort.seed must be int >= 0")
        strategy = cohort.get("strategy")
        if strategy in ALLOWED_STRATEGIES:
            validated["cohort"]["strategy"] = strategy
        else:
            errors.append(f"cohort.strategy must be one of {sorted(ALLOWED_STRATEGIES)}")
    else:
        errors.append("cohort must be dict")

    steps = plan.get("steps")
    if isinstance(steps, dict):
        steps_unknown = _unknown_keys(
            steps, {"ingestion", "normalization", "analysis", "safety", "reporting"}
        )
        if steps_unknown:
            errors.append(f"unknown steps keys: {steps_unknown}")
        for key in ["ingestion", "normalization", "analysis", "safety", "reporting"]:
            value = steps.get(key)
            if isinstance(value, bool):
                validated["steps"][key] = value
            else:
                errors.append(f"steps.{key} must be bool")
    else:
        errors.append("steps must be dict")

    output = plan.get("output")
    if isinstance(output, dict):
        output_unknown = _unknown_keys(output, {"format"})
        if output_unknown:
            errors.append(f"unknown output keys: {output_unknown}")
        output_format = output.get("format")
        if output_format in ALLOWED_OUTPUT_FORMATS:
            validated["output"]["format"] = output_format
        else:
            errors.append(f"output.format must be one of {sorted(ALLOWED_OUTPUT_FORMATS)}")
    else:
        errors.append("output must be dict")

    notes = plan.get("notes")
    if notes is None:
        validated["notes"] = ""
    elif isinstance(notes, str):
        validated["notes"] = notes
    else:
        errors.append("notes must be string")

    if not validated["steps"]["ingestion"] or not validated["steps"]["reporting"]:
        errors.append("steps.ingestion and steps.reporting must be true")

    return validated, errors

from __future__ import annotations

from autogen_core.tools import FunctionTool

from . import steps


def run_ingest() -> dict:
    """Load raw CSVs and produce base admissions, diagnoses, and labs artifacts."""
    return steps.ingest().to_dict()


def run_normalize() -> dict:
    """Normalize diagnoses and labs (mappings + unit status)."""
    return steps.normalize().to_dict()


def run_analyze() -> dict:
    """Compute features and a simple rule-based risk flag."""
    return steps.analyze().to_dict()


def run_safety() -> dict:
    """Run leakage, plausible range, dx↔lab, and missingness checks."""
    return steps.safety().to_dict()


def run_report() -> dict:
    """Generate human-readable report and audit summary artifacts."""
    return steps.report().to_dict()


TOOLS = [
    FunctionTool(run_ingest, name="ingest", description="Load raw CSVs and produce base tables."),
    FunctionTool(run_normalize, name="normalize", description="Normalize diagnoses/labs with mappings and unit checks."),
    FunctionTool(run_analyze, name="analyze", description="Compute features and rule-based risk flag."),
    FunctionTool(run_safety, name="safety", description="Safety checks (leakage, plausible ranges, missingness)."),
    FunctionTool(run_report, name="report", description="Generate cohort/feature/risk report and audit summary."),
]

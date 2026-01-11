from __future__ import annotations

import argparse
import os
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, Optional

from dotenv import load_dotenv

from autogen_core.models import ChatCompletionClient
from autogen_ext.models.openai import OpenAIChatCompletionClient

from autogenchat_demo.agents.pipeline_agents import (
    AnalysisAgent,
    CoordinatorAgent,
    IngestionAgent,
    NormalizationAgent,
    ReportAgent,
    SafetyAgent,
)
from autogenchat_demo.agents.planning_agent import PlanningAgent
from autogenchat_demo.planning.plan_schema import default_plan, validate_plan


def run_cohort_pipeline(
    dataset_dir: str = "dataset",
    n: int = 5,
    seed: int = 1,
    runs_dir: str = "runs",
) -> Dict[str, Any]:
    run_id = datetime.utcnow().strftime("%Y%m%d_%H%M%S")
    run_dir = Path(runs_dir) / run_id
    run_dir.mkdir(parents=True, exist_ok=True)

    audit_log = []
    coordinator = CoordinatorAgent("CoordinatorAgent", audit_log)
    ingestion = IngestionAgent("IngestionAgent", audit_log)
    normalization = NormalizationAgent("NormalizationAgent", audit_log)
    analysis = AnalysisAgent("AnalysisAgent", audit_log)
    safety = SafetyAgent("SafetyAgent", audit_log)
    report = ReportAgent("ReportAgent", audit_log)

    return coordinator.run_pipeline(
        dataset_dir=dataset_dir,
        n=n,
        seed=seed,
        strategy="random",
        run_dir=str(run_dir),
        ingestion=ingestion,
        normalization=normalization,
        analysis=analysis,
        safety=safety,
        report=report,
    )


def _build_model_client() -> ChatCompletionClient:
    load_dotenv()
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        raise SystemExit(
            "Missing GEMINI_API_KEY. Copy .env.example to .env and set your key."
        )

    model = os.getenv("GEMINI_MODEL", "gemini-1.5-flash").strip()
    if model.startswith("models/"):
        model = model.split("/", 1)[1]

    return OpenAIChatCompletionClient(model=model, api_key=api_key)


async def plan_and_run(
    user_query: str,
    dataset_dir: str = "dataset",
    runs_dir: str = "runs",
    model_client: Optional[ChatCompletionClient] = None,
) -> Dict[str, Any]:
    run_id = datetime.utcnow().strftime("%Y%m%d_%H%M%S")
    run_dir = Path(runs_dir) / run_id
    run_dir.mkdir(parents=True, exist_ok=True)

    audit_log: list[dict[str, Any]] = []
    coordinator = CoordinatorAgent("CoordinatorAgent", audit_log)
    ingestion = IngestionAgent("IngestionAgent", audit_log)
    normalization = NormalizationAgent("NormalizationAgent", audit_log)
    analysis = AnalysisAgent("AnalysisAgent", audit_log)
    safety = SafetyAgent("SafetyAgent", audit_log)
    report = ReportAgent("ReportAgent", audit_log)

    raw_plan: Dict[str, Any] = {}
    planning_errors: list[str] = []

    try:
        if model_client is None:
            model_client = _build_model_client()
        planner = PlanningAgent("PlanningAgent", audit_log, model_client)
        raw_plan, _raw_text = await planner.plan(user_query)
    except Exception as exc:
        planning_errors.append(f"planning_failed: {exc}")
        audit_log.append(
            {
                "timestamp": datetime.utcnow().isoformat(),
                "agent": "PlanningAgent",
                "action": "planning_request",
                "tool_called": "llm",
                "inputs_summary": {"query": user_query},
                "outputs_summary": "failed",
                "warnings": planning_errors,
            }
        )
        audit_log.append(
            {
                "timestamp": datetime.utcnow().isoformat(),
                "agent": "PlanningAgent",
                "action": "planning_raw_output",
                "tool_called": "llm",
                "inputs_summary": {"query": user_query},
                "outputs_summary": {"raw": "", "error": str(exc)},
                "warnings": planning_errors,
            }
        )

    validated_plan, validation_errors = validate_plan(raw_plan)
    errors = planning_errors + validation_errors
    if errors:
        coordinator.log(
            action="planning_validation_result",
            tool_called=None,
            inputs_summary={"query": user_query},
            outputs_summary={"errors": errors},
            warnings=errors,
        )
        validated_plan = default_plan()
    else:
        coordinator.log(
            action="planning_validation_result",
            tool_called=None,
            inputs_summary={"query": user_query},
            outputs_summary={"status": "ok"},
        )

    coordinator.log(
        action="final_plan_used",
        tool_called=None,
        inputs_summary={"query": user_query},
        outputs_summary=validated_plan,
    )

    coordinator.log(
        action="start_pipeline",
        tool_called=None,
        inputs_summary={
            "dataset_dir": dataset_dir,
            "n": validated_plan["cohort"]["n"],
            "seed": validated_plan["cohort"]["seed"],
            "strategy": validated_plan["cohort"]["strategy"],
        },
        outputs_summary="starting",
    )

    ingestion_result = ingestion.run(
        dataset_dir,
        validated_plan["cohort"]["n"],
        validated_plan["cohort"]["seed"],
        strategy=validated_plan["cohort"]["strategy"],
    )
    tables = ingestion_result["tables"]
    table_summary = ingestion_result["table_summary"]
    cohort = ingestion_result["cohort"]

    if validated_plan["steps"]["normalization"]:
        normalized = normalization.run(tables)
        tables = normalized["tables"]

    features: Dict[str, Any] = {}
    if validated_plan["steps"]["analysis"]:
        features = analysis.run(tables)

    checks: Dict[str, Any] = {"checks": [], "summary": {"pass": 0, "warn": 0, "fail": 0}}
    if validated_plan["steps"]["safety"]:
        checks = safety.run(tables, features)

    report_result = report.run(
        run_dir=str(run_dir),
        cohort=cohort,
        table_summary=table_summary,
        features=features,
        checks=checks,
    )

    coordinator.log(
        action="complete_pipeline",
        tool_called=None,
        inputs_summary={"run_dir": str(run_dir)},
        outputs_summary=report_result.get("files", {}),
    )
    return report_result


def _parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run cohort pipeline.")
    parser.add_argument("--dataset-dir", default="dataset")
    parser.add_argument("--n", type=int, default=5)
    parser.add_argument("--seed", type=int, default=1)
    parser.add_argument("--runs-dir", default="runs")
    return parser.parse_args()


def main() -> None:
    args = _parse_args()
    result = run_cohort_pipeline(
        dataset_dir=args.dataset_dir,
        n=args.n,
        seed=args.seed,
        runs_dir=args.runs_dir,
    )
    files = result.get("files", {})
    print("Pipeline complete. Output files:")
    for key, path in files.items():
        print(f"- {key}: {path}")


if __name__ == "__main__":
    main()

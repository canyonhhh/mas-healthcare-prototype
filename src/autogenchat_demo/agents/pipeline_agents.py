from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from typing import Any, Dict, List

from autogenchat_demo.tools import mimic_tools


def _timestamp() -> str:
    return datetime.utcnow().isoformat()


@dataclass
class BaseAgent:
    name: str
    audit_log: List[Dict[str, Any]]

    def log(
        self,
        action: str,
        tool_called: str | None,
        inputs_summary: Any,
        outputs_summary: Any,
        warnings: List[str] | None = None,
    ) -> None:
        self.audit_log.append(
            {
                "timestamp": _timestamp(),
                "agent": self.name,
                "action": action,
                "tool_called": tool_called,
                "inputs_summary": inputs_summary,
                "outputs_summary": outputs_summary,
                "warnings": warnings or [],
            }
        )


class IngestionAgent(BaseAgent):
    def run(self, dataset_dir: str, n: int, seed: int, strategy: str = "random") -> Dict[str, Any]:
        self.log(
            action="select_cohort",
            tool_called="pick_cohort",
            inputs_summary={
                "dataset_dir": dataset_dir,
                "n": n,
                "seed": seed,
                "strategy": strategy,
            },
            outputs_summary="pending",
        )
        cohort = mimic_tools.pick_cohort(dataset_dir, n, seed, strategy=strategy)
        self.log(
            action="select_cohort",
            tool_called="pick_cohort",
            inputs_summary={
                "dataset_dir": dataset_dir,
                "n": n,
                "seed": seed,
                "strategy": strategy,
            },
            outputs_summary={"hadm_count": len(cohort.get("hadm_ids", []))},
        )

        self.log(
            action="load_tables",
            tool_called="load_hosp_tables",
            inputs_summary={"hadm_ids": cohort.get("hadm_ids", [])},
            outputs_summary="pending",
        )
        load_result = mimic_tools.load_hosp_tables(dataset_dir, cohort.get("hadm_ids", []))
        self.log(
            action="load_tables",
            tool_called="load_hosp_tables",
            inputs_summary={"hadm_ids": cohort.get("hadm_ids", [])},
            outputs_summary=load_result.get("table_summary", {}),
        )
        return {"cohort": cohort, "tables": load_result["tables"], "table_summary": load_result["table_summary"]}


class NormalizationAgent(BaseAgent):
    def run(self, tables: Dict[str, Any]) -> Dict[str, Any]:
        self.log(
            action="normalize_tables",
            tool_called="normalize_hosp",
            inputs_summary={"tables": list(tables.keys())},
            outputs_summary="pending",
        )
        result = mimic_tools.normalize_hosp(tables)
        self.log(
            action="normalize_tables",
            tool_called="normalize_hosp",
            inputs_summary={"tables": list(tables.keys())},
            outputs_summary=result.get("mapping_stats", {}),
        )
        return result


class AnalysisAgent(BaseAgent):
    def run(self, tables: Dict[str, Any]) -> Dict[str, Any]:
        self.log(
            action="compute_features",
            tool_called="compute_features",
            inputs_summary={"tables": list(tables.keys())},
            outputs_summary="pending",
        )
        result = mimic_tools.compute_features(tables)
        self.log(
            action="compute_features",
            tool_called="compute_features",
            inputs_summary={"tables": list(tables.keys())},
            outputs_summary=result.get("features_summary", {}),
        )
        return result


class SafetyAgent(BaseAgent):
    def run(self, tables: Dict[str, Any], features: Dict[str, Any]) -> Dict[str, Any]:
        self.log(
            action="run_safety_checks",
            tool_called="run_safety_checks",
            inputs_summary={"tables": list(tables.keys())},
            outputs_summary="pending",
        )
        result = mimic_tools.run_safety_checks(tables, features)
        self.log(
            action="run_safety_checks",
            tool_called="run_safety_checks",
            inputs_summary={"tables": list(tables.keys())},
            outputs_summary=result.get("summary", {}),
        )
        return result


class ReportAgent(BaseAgent):
    def run(
        self,
        run_dir: str,
        cohort: Dict[str, Any],
        table_summary: Dict[str, Any],
        features: Dict[str, Any],
        checks: Dict[str, Any],
    ) -> Dict[str, Any]:
        self.log(
            action="write_report",
            tool_called="write_report",
            inputs_summary={"run_dir": run_dir},
            outputs_summary="pending",
        )
        result = mimic_tools.write_report(
            run_dir=run_dir,
            cohort=cohort,
            table_summary=table_summary,
            features=features,
            checks=checks,
            audit_log=self.audit_log,
        )
        self.log(
            action="write_report",
            tool_called="write_report",
            inputs_summary={"run_dir": run_dir},
            outputs_summary=result.get("files", {}),
        )
        return result


class CoordinatorAgent(BaseAgent):
    def run_pipeline(
        self,
        dataset_dir: str,
        n: int,
        seed: int,
        strategy: str,
        run_dir: str,
        ingestion: IngestionAgent,
        normalization: NormalizationAgent,
        analysis: AnalysisAgent,
        safety: SafetyAgent,
        report: ReportAgent,
    ) -> Dict[str, Any]:
        self.log(
            action="start_pipeline",
            tool_called=None,
            inputs_summary={"dataset_dir": dataset_dir, "n": n, "seed": seed},
            outputs_summary="starting",
        )

        ingestion_result = ingestion.run(dataset_dir, n, seed, strategy=strategy)
        normalized = normalization.run(ingestion_result["tables"])
        tables_with_norm = normalized["tables"]
        features = analysis.run(tables_with_norm)
        checks = safety.run(tables_with_norm, features)
        report_result = report.run(
            run_dir=run_dir,
            cohort=ingestion_result["cohort"],
            table_summary=ingestion_result["table_summary"],
            features=features,
            checks=checks,
        )

        self.log(
            action="complete_pipeline",
            tool_called=None,
            inputs_summary={"run_dir": run_dir},
            outputs_summary=report_result.get("files", {}),
        )
        return report_result

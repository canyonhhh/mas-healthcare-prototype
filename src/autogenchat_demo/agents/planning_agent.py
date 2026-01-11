from __future__ import annotations

import json
from typing import Any, Dict, Tuple

from autogen_core.models import SystemMessage, UserMessage
from autogen_core.models import ChatCompletionClient

from autogenchat_demo.agents.pipeline_agents import BaseAgent


PLANNING_SYSTEM_PROMPT = """You are a planning agent. Output ONLY strict JSON with no markdown.
Schema:
{
  "plan_version": int,
  "pipeline": "cohort_report",
  "cohort": {"n": int (1..50), "seed": int (>=0), "strategy": "random" | "first_n" | "recent"},
  "steps": {"ingestion": bool, "normalization": bool, "analysis": bool, "safety": bool, "reporting": bool},
  "output": {"format": "md" | "json" | "both"},
  "notes": "optional string"
}
Rules:
- No extra keys.
- No tool calls, no data access.
- Keep steps minimal and safe; ingestion and reporting must be true.
"""


class PlanningAgent(BaseAgent):
    def __init__(self, name: str, audit_log: list[dict[str, Any]], model_client: ChatCompletionClient):
        super().__init__(name, audit_log)
        self.model_client = model_client

    async def plan(self, user_query: str) -> Tuple[Dict[str, Any], str]:
        self.log(
            action="planning_request",
            tool_called="llm",
            inputs_summary={"query": user_query},
            outputs_summary="pending",
        )
        messages = [
            SystemMessage(content=PLANNING_SYSTEM_PROMPT),
            UserMessage(content=user_query, source="user"),
        ]
        response = await self.model_client.create(
            messages=messages,
            extra_create_args={"temperature": 0},
        )
        raw_text = response.content if isinstance(response.content, str) else json.dumps(response.content)
        self.log(
            action="planning_raw_output",
            tool_called="llm",
            inputs_summary={"query": user_query},
            outputs_summary={"raw": raw_text[:1000]},
        )
        try:
            plan = json.loads(raw_text)
        except json.JSONDecodeError:
            plan = {}
        return plan, raw_text

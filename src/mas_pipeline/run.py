from __future__ import annotations

import asyncio
import json
import os
from pathlib import Path

from dotenv import load_dotenv

from autogen_agentchat.agents import AssistantAgent
from autogen_agentchat.conditions import TextMentionTermination
from autogen_agentchat.messages import TextMessage
from autogen_agentchat.teams import RoundRobinGroupChat
from autogen_ext.models.openai import OpenAIChatCompletionClient

from .contracts import PipelinePaths
from .config import get_config
from .tools import TOOLS


def _get_tool(name: str):
    for t in TOOLS:
        if t.name == name:
            return t
    raise KeyError(name)


def _make_agent(name: str, tool_name: str, instructions: str, model_client: OpenAIChatCompletionClient) -> AssistantAgent:
    return AssistantAgent(
        name=name,
        model_client=model_client,
        tools=[_get_tool(tool_name)],
        system_message=instructions,
        max_tool_iterations=1,
    )


def build_team(model_client: OpenAIChatCompletionClient) -> RoundRobinGroupChat:
    ingestion_agent = _make_agent(
        "ingestion_agent",
        "ingest",
        "You are the Ingestion Agent. Call the ingest tool exactly once to load base tables. Summarize key counts. If the tool output shows stop=true, include PIPELINE_STOP.",
        model_client,
    )
    normalization_agent = _make_agent(
        "normalization_agent",
        "normalize",
        "You are the Normalization Agent. Call the normalize tool exactly once to map ICD and lab items. Summarize mapping coverage and unit consistency. If stop=true, include PIPELINE_STOP.",
        model_client,
    )
    analysis_agent = _make_agent(
        "analysis_agent",
        "analyze",
        "You are the Analysis Agent. Call the analyze tool exactly once to compute features and risk flag. Summarize results. If stop=true, include PIPELINE_STOP.",
        model_client,
    )
    safety_agent = _make_agent(
        "safety_agent",
        "safety",
        "You are the Safety/Quality Agent. Call the safety tool exactly once. If the tool output indicates failures or stop=true, include PIPELINE_STOP so the round-robin halts.",
        model_client,
    )
    reporting_agent = _make_agent(
        "reporting_agent",
        "report",
        "You are the Reporting Agent. Call the report tool exactly once to write report.md and audit_summary.md. Always include PIPELINE_STOP at the end.",
        model_client,
    )

    return RoundRobinGroupChat(
        participants=[
            ingestion_agent,
            normalization_agent,
            analysis_agent,
            safety_agent,
            reporting_agent,
        ],
        termination_condition=TextMentionTermination("PIPELINE_STOP"),
        max_turns=5,
    )


async def _arun() -> None:
    load_dotenv()
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        raise SystemExit("Missing GEMINI_API_KEY. Copy .env.example to .env and set your key.")

    model = os.getenv("GEMINI_MODEL", "gemini-1.5-flash").strip()
    if model.startswith("models/"):
        model = model.split("/", 1)[1]

    model_client = OpenAIChatCompletionClient(model=model, api_key=api_key)

    # Always use default config; no user goal parsing.
    goal = "Run the MAS pipeline now."
    paths = PipelinePaths.default(Path("."))
    paths.artifacts_dir.mkdir(parents=True, exist_ok=True)
    (paths.artifacts_dir / "config_override.json").write_text(
        json.dumps(get_config(), indent=2), encoding="utf-8"
    )

    team = build_team(model_client)

    print("Running MAS pipeline with RoundRobinGroupChat...")
    result = await team.run(task=TextMessage(content=goal, source="user"))
    print("Pipeline finished. Stop reason:", result.stop_reason)
    print("See artifacts/ for outputs.")


def run() -> None:
    asyncio.run(_arun())


if __name__ == "__main__":
    run()

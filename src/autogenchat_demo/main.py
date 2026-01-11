import asyncio
import os
from typing import Optional

from dotenv import load_dotenv

from autogen_agentchat.agents import AssistantAgent
from autogen_agentchat.messages import TextMessage
from autogen_core import CancellationToken
from autogen_ext.models.openai import OpenAIChatCompletionClient

from autogenchat_demo.pipeline import plan_and_run, run_cohort_pipeline


def _parse_run_command(command: str) -> dict:
    parts = command.strip().split()
    if len(parts) < 2 or parts[0] != "run" or parts[1] != "cohort":
        return {}
    params = {"n": 5, "seed": 1}
    for part in parts[2:]:
        if "=" not in part:
            continue
        key, value = part.split("=", 1)
        if key in {"n", "seed"}:
            try:
                params[key] = int(value)
            except ValueError:
                continue
    return params


def _parse_plan_command(command: str) -> Optional[str]:
    if not command.lower().startswith("plan "):
        return None
    query = command[5:].strip()
    if len(query) >= 2 and query[0] == query[-1] == '"':
        query = query[1:-1].strip()
    return query or None


async def _chat_loop(assistant: AssistantAgent, model_client: OpenAIChatCompletionClient) -> None:
    print("Type exit, quit, or q to end the chat.")
    while True:
        try:
            prompt = input("You: ").strip()
        except EOFError:
            print()
            break
        if not prompt:
            continue
        if prompt.lower() in {"exit", "quit", "q"}:
            break
        plan_query = _parse_plan_command(prompt)
        if plan_query:
            result = await plan_and_run(plan_query, model_client=model_client)
            files = result.get("files", {})
            print("Pipeline complete. Output files:")
            for key, path in files.items():
                print(f"- {key}: {path}")
            continue

        run_params = _parse_run_command(prompt)
        if run_params:
            result = run_cohort_pipeline(n=run_params["n"], seed=run_params["seed"])
            files = result.get("files", {})
            print("Pipeline complete. Output files:")
            for key, path in files.items():
                print(f"- {key}: {path}")
            continue

        response = await assistant.on_messages(
            [TextMessage(content=prompt, source="user")],
            cancellation_token=CancellationToken(),
        )
        print(f"Assistant: {response.chat_message.to_text()}")


def run() -> None:
    load_dotenv()

    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        raise SystemExit(
            "Missing GEMINI_API_KEY. Copy .env.example to .env and set your key."
        )

    model = os.getenv("GEMINI_MODEL", "gemini-1.5-flash").strip()
    if model.startswith("models/"):
        model = model.split("/", 1)[1]

    model_client = OpenAIChatCompletionClient(
        model=model,
        api_key=api_key,
    )
    assistant = AssistantAgent("assistant", model_client=model_client, system_message=None)

    asyncio.run(_chat_loop(assistant, model_client))


if __name__ == "__main__":
    run()

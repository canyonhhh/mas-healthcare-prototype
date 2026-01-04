import asyncio
import os

from dotenv import load_dotenv

from autogen_agentchat.agents import AssistantAgent
from autogen_agentchat.messages import TextMessage
from autogen_core import CancellationToken
from autogen_ext.models.openai import OpenAIChatCompletionClient


async def _chat_loop(assistant: AssistantAgent) -> None:
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

    asyncio.run(_chat_loop(assistant))


if __name__ == "__main__":
    run()

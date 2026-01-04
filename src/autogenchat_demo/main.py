import os
from dotenv import load_dotenv

try:
    from autogen.agentchat import AssistantAgent, UserProxyAgent
except ImportError:  # pragma: no cover - fallback for older autogen layouts
    from autogen import AssistantAgent, UserProxyAgent


def _is_termination_msg(message):
    content = (message.get("content") or "").strip().lower()
    return content in {"exit", "quit", "q"}


def run():
    load_dotenv()

    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        raise SystemExit(
            "Missing GEMINI_API_KEY. Copy .env.example to .env and set your key."
        )

    model = os.getenv("GEMINI_MODEL", "gemini-1.5-pro")

    llm_config = {
        "config_list": [
            {
                "model": model,
                "api_key": api_key,
                "api_type": "google",
            }
        ],
        "temperature": 0.2,
    }

    assistant = AssistantAgent("assistant", llm_config=llm_config)
    user = UserProxyAgent(
        "user",
        human_input_mode="ALWAYS",
        is_termination_msg=_is_termination_msg,
        code_execution_config=False,
    )

    user.initiate_chat(assistant, message="Hi! What can you help me with today?")


if __name__ == "__main__":
    run()

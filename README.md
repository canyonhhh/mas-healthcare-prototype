# mas-healthcare-prototype

Autogen agentchat demo wired to Gemini using the OpenAI-compatible endpoint.

## Setup

```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

Create a `.env` file:

```bash
cp .env.example .env
```

Then add your Gemini API key to `.env`. The default base URL targets the
OpenAI-compatible Gemini endpoint; override `GEMINI_BASE_URL` if needed.

## Run

```bash
pip install -e .
autogenchat
```

Or run directly without installing:

```bash
PYTHONPATH=src python -m autogenchat_demo.main
```

Type `exit`, `quit`, or `q` to end the chat.

## Run the MAS pipeline (round robin)

```bash
pip install -e .
mas-pipeline
```

Outputs are written to `artifacts/` (registry.json, audit.jsonl, features, safety_report.json, report.md).
At runtime you’ll be prompted for a goal; press Enter to accept the default, or set `MAS_GOAL="warn on future labs; LOS 96 hours; abnormal lab threshold 5"` to tweak thresholds via the goal parser.

## Notes

This project uses `autogen-ext` with the OpenAI-compatible Gemini endpoint:
`https://generativelanguage.googleapis.com/v1beta/openai/`.

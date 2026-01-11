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

### Cohort pipeline commands

Inside the REPL you can run deterministic pipelines:

```text
run cohort n=5 seed=1
plan "cohort report for 5 admissions with safety checks"
```

You can also run the pipeline directly:

```bash
python -m autogenchat_demo.pipeline --n 5 --seed 1
python -m autogenchat_demo.smoke_test_planning
```

## Notes

This project uses `autogen-ext` with the OpenAI-compatible Gemini endpoint:
`https://generativelanguage.googleapis.com/v1beta/openai/`.

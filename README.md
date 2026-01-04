# mas-healthcare-prototype

Autogen agentchat demo wired to Gemini using an API key.

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

Then add your Gemini API key to `.env`.

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

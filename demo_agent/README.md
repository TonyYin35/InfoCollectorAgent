# Demo Agent

A conversational chat agent built with LangGraph and Google Gemini. It uses Gemini's native Google Search grounding to answer questions with up-to-date web information, and supports streaming responses with extended thinking.

## Prerequisites

- Python 3.13+
- [uv](https://docs.astral.sh/uv/) package manager
- A Google API key with Gemini API access

## Setup

1. Create a virtual environment and install dependencies:

```bash
uv venv
uv pip install -r requirements.txt
```

2. Create a `.env` file in this directory with your API key:

```
GOOGLE_API_KEY=your_api_key_here
```

## Usage

```bash
uv run python chat.py
```

Type your questions at the `You:` prompt. The agent will search the web and respond with grounded answers. Type `quit` to exit.

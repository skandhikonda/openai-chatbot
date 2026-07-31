# OpenAI Chatbot

A simple FastAPI-powered chatbot that uses OpenAI's Chat Completions API and provides an interactive browser-based chat interface.

## Features

- Browser-based chat UI served from FastAPI
- Session-based conversation history using cookies
- `exit` command closes the session cleanly
- Easy setup with `.env` for the OpenAI API key

## Requirements

- Python 3.10+ recommended
- `requirements.txt` includes:
  - `fastapi`
  - `uvicorn`
  - `openai`
  - `python-dotenv`

## Setup

1. Create a `.env` file in the project folder with:

```env
OPENAI_API_KEY=your_openai_api_key_here
```

2. Install dependencies:

```bash
pip install -r requirements.txt
```

## Run

Start the app with:

```bash
python simple_chatbot.py
```

Then open your browser at:

```text
http://127.0.0.1:8000/
```

## Usage

- Type a message and press `Send` or Enter
- The bot responds in the browser UI
- Type `exit` to terminate the current session

## Notes

- The session is stored in memory and resets when the app restarts.
- For production, consider adding persistent session storage and better API error handling.

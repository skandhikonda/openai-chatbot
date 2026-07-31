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
http://mychatbot.local:8000/
```

## Usage

- Type a message and press `Send` or Enter
- The bot responds in the browser UI
- Type `exit` to terminate the current session

## How it works

The app is implemented in `simple_chatbot.py` and uses FastAPI to serve both the chat page and the API endpoints.

- `load_dotenv()` loads the OpenAI API key from `.env`
- `OpenAI(api_key=api_key)` creates the OpenAI client
- `session_histories` keeps conversation state in memory using a session cookie
- The `/` route returns an HTML page with a simple chat UI
- The `/chat` route receives JSON messages, forwards them to OpenAI, and returns the assistant reply

### Session handling

- Each new visitor gets a `session_id` cookie
- Session history is stored in `session_histories[session_id]`
- Conversation history is sent to OpenAI so the assistant remembers context
- Typing `exit` clears the session and removes the session cookie

### Frontend behavior

- The HTML page includes JavaScript to send messages to `/chat`
- User messages and bot replies are appended to the browser chat log
- If the API returns `ended: true`, the UI disables input and asks the user to refresh

## Notes

- The session is stored in memory and resets when the app restarts.
- This implementation is intended for learning and local experimentation.
- For production, consider adding:
  - persistent session storage
  - stronger input validation
  - rate limiting
  - more robust OpenAI error handling

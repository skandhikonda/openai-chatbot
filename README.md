# OpenAI Chatbot

This project is a FastAPI-based chatbot that uses OpenAI's Chat Completions API through a dedicated service layer. The FastAPI app focuses on handling HTTP requests and session state, while the service layer is responsible for calling OpenAI, formatting prompts, handling retries, and evaluating responses.

## What this project contains

- A FastAPI web app in [simple_chatbot.py](simple_chatbot.py)
- A reusable chat service in [chatbot_app/services/chat_service.py](chatbot_app/services/chat_service.py)
- Structured response models in [chatbot_app/models/chat_models.py](chatbot_app/models/chat_models.py)
- A prompt template in [chatbot_app/prompts/system_prompt.txt](chatbot_app/prompts/system_prompt.txt)

## Main features

- Browser-based chat UI served by FastAPI
- Session-based conversation history stored in memory using cookies
- A service layer that isolates OpenAI integration from the API layer
- Prompt templating loaded from a text file
- Structured JSON responses from the model
- Basic response evaluation for quality checks
- Logging for requests and service errors
- Retry handling for transient OpenAI failures
- An `exit` command that ends the current session cleanly

## Architecture overview

### FastAPI app
The file [simple_chatbot.py](simple_chatbot.py) contains the web layer:
- serves the UI at `/`
- receives chat requests at `/chat`
- manages session cookies and in-memory history
- returns JSON responses back to the browser

### Chat service
The service in [chatbot_app/services/chat_service.py](chatbot_app/services/chat_service.py) is responsible for:
- creating the OpenAI client
- building the request payload
- sending the prompt and conversation history to the model
- parsing the model output
- retrying requests when temporary API issues occur

### Prompt template
The prompt template lives in [chatbot_app/prompts/system_prompt.txt](chatbot_app/prompts/system_prompt.txt). It instructs the model to return a JSON object with:
- `reply`
- `confidence`
- `ended`

### Structured outputs
The application uses Pydantic models in [chatbot_app/models/chat_models.py](chatbot_app/models/chat_models.py) to represent:
- the chat response payload
- the evaluation result for the generated reply

### Logging and evaluation
The service logs request failures and retries, and it evaluates each generated response with a lightweight quality check. The evaluation result is returned alongside the reply so the API layer can expose it to the client if needed.

## Requirements

- Python 3.10+ recommended
- The dependencies in [requirements.txt](requirements.txt) include:
  - `fastapi`
  - `uvicorn`
  - `openai`
  - `python-dotenv`
  - `pydantic`
  - `pytest`

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

- The session data is stored in memory and resets when the app restarts.
- This implementation is intended for learning and local experimentation.
- For production, consider adding persistent session storage, stronger validation, rate limiting, and more advanced evaluation logic.

# OpenAI Chatbot

A FastAPI-powered chatbot that uses OpenAI's API through a dedicated service layer. The application serves a simple browser-based chat interface while keeping OpenAI integration, prompt management, retries, logging, and response evaluation separate from the web layer.

## Project Overview

This project demonstrates how to build a production-style Python AI app with a clean separation between:

- the FastAPI web layer
- the chat service layer
- the prompt and response models
- the evaluation and logging utilities

The app allows users to send messages, maintain a short conversation history, and receive structured responses that include confidence and evaluation metadata.

## Architecture

The project follows a simple layered architecture:

1. FastAPI app layer
   - serves the web UI at `/`
   - receives chat requests at `/chat`
   - manages session cookies and in-memory chat history

2. Service layer
   - `ChatService` handles OpenAI requests
   - builds the prompt payload
   - retries transient failures
   - parses model output and evaluates responses

3. Model layer
   - `ChatResponse` and `ChatEvaluation` define structured response objects

4. Prompt layer
   - prompt instructions are loaded from a text file for easier maintenance

This design keeps the API layer focused on request handling instead of embedding all LLM logic directly in the route handlers.

## Folder Structure

```text
openai-chatbot/
├── chatbot_app/
│   ├── models/
│   ├── prompts/
│   └── services/
├── tests/
├── requirements.txt
├── simple_chatbot.py
└── README.md
```

## Installation

### Prerequisites

- Python 3.10+
- A virtual environment
- An OpenAI API key

### Setup

```bash
python -m venv .venv
```

Activate the environment:

```powershell
.\.venv\Scripts\Activate.ps1
```

Install dependencies:

```bash
pip install -r requirements.txt
```

## Configuration

Create a `.env` file in the project root with:

```env
OPENAI_API_KEY=your_openai_api_key_here
OPENAI_MODEL=gpt-3.5-turbo
```

## Running Locally

Start the app with:

```bash
python simple_chatbot.py
```

Then open:

```text
http://127.0.0.1:8000/
```

## Example Output

```text
You: What is the capital of France?
Bot: Paris.
```

The API also returns structured metadata including confidence and evaluation details for the generated response.

## Future Enhancements

Possible improvements include:

- persistent session storage instead of in-memory history
- richer prompt templates and conversation memory
- support for streaming responses
- stronger validation and error handling
- authentication and user management for multi-user deployments

## Technologies Used

- Python
- FastAPI
- OpenAI SDK
- Pydantic
- Python-dotenv
- pytest

## Testing

Run the tests with:

```bash
pytest
```

import os
import uuid
from typing import Dict, List, Optional
from dotenv import load_dotenv
from fastapi import Cookie, FastAPI, HTTPException, Request, Response
from fastapi.responses import HTMLResponse, JSONResponse
from pydantic import BaseModel
from openai import OpenAI
import uvicorn

load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")

if not api_key:
    raise RuntimeError("OPENAI_API_KEY not found in environment. Please create a .env file.")

client = OpenAI(api_key=api_key)
app = FastAPI()
session_histories: Dict[str, List[dict]] = {}

HTML_PAGE = """<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>OpenAI Chatbot</title>
  <style>
    body { font-family: Arial, sans-serif; background: #f4f7fb; margin: 0; padding: 0; }
    .container { max-width: 720px; margin: 0 auto; padding: 24px; }
    .chat-box { background: #fff; border-radius: 12px; box-shadow: 0 20px 40px rgba(0, 0, 0, 0.08); padding: 20px; }
    .message { margin-bottom: 16px; }
    .message.bot { color: #1f2937; }
    .message.user { color: #0f4c81; text-align: right; }
    .message.system { color: #6b7280; font-size: 0.95rem; }
    #messages { min-height: 320px; margin-bottom: 16px; overflow-y: auto; }
    #userInput { width: calc(100% - 96px); padding: 12px; border: 1px solid #d1d5db; border-radius: 8px; }
    #sendButton { padding: 12px 18px; margin-left: 8px; border: none; border-radius: 8px; background: #2563eb; color: white; cursor: pointer; }
    #sendButton:disabled { background: #93c5fd; cursor: not-allowed; }
  </style>
</head>
<body>
  <div class="container">
    <h1>OpenAI Chatbot</h1>
    <div class="chat-box">
      <div id="messages"></div>
      <div>
        <input id="userInput" type="text" placeholder="Type your message here..." autocomplete="off" />
        <button id="sendButton">Send</button>
      </div>
    </div>
  </div>
  <script>
    const messages = document.getElementById('messages');
    const input = document.getElementById('userInput');
    const button = document.getElementById('sendButton');

    function appendMessage(role, text) {
      const element = document.createElement('div');
      element.className = 'message ' + role;
      element.textContent = (role === 'user' ? 'You: ' : role === 'bot' ? 'Bot: ' : 'System: ') + text;
      messages.appendChild(element);
      messages.scrollTop = messages.scrollHeight;
    }

    async function sendMessage() {
      const message = input.value.trim();
      if (!message) {
        return;
      }

      appendMessage('user', message);
      input.value = '';
      button.disabled = true;

      try {
        const response = await fetch('/chat', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ message }),
        });

        if (!response.ok) {
          throw new Error('Chat request failed');
        }

        const data = await response.json();
        appendMessage('bot', data.reply);

        if (data.ended) {
          appendMessage('system', 'Chat ended. Refresh the page to start a new session.');
          input.disabled = true;
          button.disabled = true;
        }
      } catch (err) {
        appendMessage('system', 'Error: ' + err.message);
      } finally {
        button.disabled = false;
      }
    }

    button.addEventListener('click', sendMessage);
    input.addEventListener('keydown', (event) => {
      if (event.key === 'Enter') {
        sendMessage();
      }
    });

    appendMessage('system', 'Type a message to begin chatting. Type "exit" to end the session.');
  </script>
</body>
</html>"""

class ChatRequest(BaseModel):
    message: str


@app.get('/', response_class=HTMLResponse)
def index(response: Response, session_id: Optional[str] = Cookie(None)):
    if not session_id or session_id not in session_histories:
        session_id = str(uuid.uuid4())
        session_histories[session_id] = [
            {"role": "system", "content": "You are a helpful assistant."}
        ]
    response.set_cookie(key='session_id', value=session_id, httponly=True)
    return HTML_PAGE


@app.post('/chat')
def chat(request: ChatRequest, response: Response, session_id: Optional[str] = Cookie(None)):
    if not session_id or session_id not in session_histories:
        session_id = str(uuid.uuid4())
        session_histories[session_id] = [
            {"role": "system", "content": "You are a helpful assistant."}
        ]

    history = session_histories[session_id]
    user_message = request.message.strip()

    if not user_message:
        raise HTTPException(status_code=400, detail='Message cannot be empty.')

    if user_message.lower() == 'exit':
        session_histories.pop(session_id, None)
        response.set_cookie(key='session_id', value='', max_age=0)
        return JSONResponse({"reply": "Goodbye! Your session has ended.", "ended": True})

    history.append({"role": "user", "content": user_message})

    try:
        completion = client.chat.completions.create(
            model='gpt-3.5-turbo',
            messages=history,
            max_tokens=150,
        )
        assistant_message = completion.choices[0].message.content.strip()
        history.append({"role": "assistant", "content": assistant_message})
        response.set_cookie(key='session_id', value=session_id, httponly=True)
        return {"reply": assistant_message, "ended": False}
    except Exception as err:
        raise HTTPException(status_code=500, detail=str(err))


if __name__ == '__main__':
    uvicorn.run('simple_chatbot:app', host='127.0.0.1', port=8000, reload=True)

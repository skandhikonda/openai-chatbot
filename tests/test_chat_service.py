import json
import sys
from pathlib import Path
from types import SimpleNamespace

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from chatbot_app.services.chat_service import ChatService


class FakeCompletions:
    def __init__(self, payload):
        self._payload = payload

    def create(self, **kwargs):
        return SimpleNamespace(
            choices=[SimpleNamespace(message=SimpleNamespace(content=json.dumps(self._payload)))]
        )


class FakeClient:
    def __init__(self, payload):
        self.chat = SimpleNamespace(completions=FakeCompletions(payload))


def test_generate_reply_returns_structured_response():
    service = ChatService(client=FakeClient({"reply": "Hello there", "confidence": 0.91, "ended": False}))

    response = service.generate_reply(
        history=[{"role": "system", "content": "You are a helpful assistant."}],
        user_message="Say hello",
    )

    assert response.reply == "Hello there"
    assert response.confidence == 0.91
    assert response.ended is False
    assert response.evaluation.passed is True


def test_evaluate_response_flags_short_answers():
    service = ChatService(client=FakeClient({"reply": "Hi", "confidence": 0.2, "ended": False}))

    evaluation = service.evaluate_response("Hi")

    assert evaluation.passed is False
    assert "too_short" in evaluation.issues

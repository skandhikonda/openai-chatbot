import json
import logging
import os
from pathlib import Path
from typing import Any, Dict, List, Optional

from dotenv import load_dotenv
from openai import OpenAI
from openai import APIError, RateLimitError, Timeout

from chatbot_app.models.chat_models import ChatEvaluation, ChatResponse


load_dotenv()

logger = logging.getLogger("chatbot")
logger.setLevel(logging.INFO)
if not logger.handlers:
    handler = logging.StreamHandler()
    handler.setFormatter(logging.Formatter("%(asctime)s %(levelname)s %(name)s %(message)s"))
    logger.addHandler(handler)


class ChatService:
    def __init__(self, client: Optional[OpenAI] = None):
        self.client = client or OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        self.prompt_template = self._load_prompt_template()
        self.max_retries = 3
        self.retry_delay_seconds = 1.0

    def _load_prompt_template(self) -> str:
        prompt_path = Path(__file__).resolve().parents[1] / "prompts" / "system_prompt.txt"
        return prompt_path.read_text(encoding="utf-8")

    def _build_messages(self, history: List[Dict[str, str]], user_message: str) -> List[Dict[str, str]]:
        messages = list(history)
        messages.append({"role": "user", "content": user_message})
        return messages

    def _build_request_payload(self, history: List[Dict[str, str]], user_message: str) -> Dict[str, Any]:
        messages = [
            {"role": "system", "content": self.prompt_template},
            *self._build_messages(history, user_message),
        ]
        return {
            "model": os.getenv("OPENAI_MODEL", "gpt-3.5-turbo"),
            "messages": messages,
            "temperature": 0.2,
            "max_tokens": 220,
            "response_format": {"type": "json_object"},
        }

    def _parse_model_output(self, raw_output: str) -> Dict[str, Any]:
        try:
            payload = json.loads(raw_output)
        except json.JSONDecodeError as exc:
            logger.warning("Model output was not valid JSON: %s", exc)
            payload = {"reply": raw_output, "confidence": 0.4, "ended": False}
        return payload

    def generate_reply(self, history: List[Dict[str, str]], user_message: str) -> ChatResponse:
        payload = self._build_request_payload(history, user_message)
        last_error: Optional[Exception] = None

        for attempt in range(self.max_retries):
            try:
                completion = self.client.chat.completions.create(**payload)
                raw_content = completion.choices[0].message.content or "{}"
                parsed = self._parse_model_output(raw_content)
                reply = str(parsed.get("reply", "I'm here to help.")).strip()
                confidence = float(parsed.get("confidence", 0.5))
                ended = bool(parsed.get("ended", False))
                evaluation = self.evaluate_response(reply)
                return ChatResponse(
                    reply=reply,
                    confidence=min(max(confidence, 0.0), 1.0),
                    ended=ended,
                    evaluation=evaluation,
                )
            except (APIError, RateLimitError, Timeout, ConnectionError) as exc:
                last_error = exc
                logger.warning("OpenAI call failed on attempt %s/%s: %s", attempt + 1, self.max_retries, exc)
                if attempt < self.max_retries - 1:
                    import time

                    time.sleep(self.retry_delay_seconds)
                else:
                    logger.exception("OpenAI call failed after retries")
                    raise RuntimeError("OpenAI request failed after retries") from exc

        if last_error:
            raise RuntimeError("OpenAI request failed") from last_error
        raise RuntimeError("OpenAI request failed")

    def evaluate_response(self, reply: str) -> ChatEvaluation:
        issues: List[str] = []
        score = 0.8
        words = len(reply.split())
        if words < 2:
            score -= 0.2
            issues.append("too_short")
        if len(reply) < 10:
            score -= 0.1
            issues.append("too_terse")
        if not reply.endswith((".", "!", "?")) and len(reply) > 0:
            issues.append("missing_punctuation")
            score -= 0.05
        score = max(0.0, min(1.0, score))
        return ChatEvaluation(
            passed=score >= 0.6,
            score=score,
            issues=issues,
            summary="Response quality evaluation completed.",
        )

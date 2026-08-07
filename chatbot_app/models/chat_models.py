from typing import List

from pydantic import BaseModel, Field


class ChatEvaluation(BaseModel):
    passed: bool
    score: float = Field(ge=0.0, le=1.0)
    issues: List[str] = Field(default_factory=list)
    summary: str


class ChatResponse(BaseModel):
    reply: str
    confidence: float = Field(ge=0.0, le=1.0)
    ended: bool = False
    evaluation: ChatEvaluation

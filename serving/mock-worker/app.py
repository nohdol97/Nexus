from __future__ import annotations

import os
import time
import uuid

from fastapi import FastAPI
from pydantic import BaseModel, Field

MODEL_NAME = os.getenv("WORKER_MODEL_NAME", "mock-worker")

app = FastAPI(title="Mock Model Worker", version="0.1.0")


class Message(BaseModel):
    role: str
    content: str


class ChatCompletionRequest(BaseModel):
    model: str = Field(default=MODEL_NAME)
    messages: list[Message]
    temperature: float | None = None
    max_tokens: int | None = None
    stream: bool | None = None


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@app.get("/v1/models")
def list_models() -> dict[str, object]:
    return {
        "object": "list",
        "data": [{"id": MODEL_NAME, "object": "model"}],
    }


@app.post("/v1/chat/completions")
def chat_completions(payload: ChatCompletionRequest) -> dict[str, object]:
    model = payload.model or MODEL_NAME
    user_text = ""
    for message in reversed(payload.messages):
        if message.role == "user":
            user_text = message.content
            break

    content = f"mock response: {user_text}" if user_text else "mock response"
    now = int(time.time())
    return {
        "id": f"mock-worker-{uuid.uuid4()}",
        "object": "chat.completion",
        "created": now,
        "model": model,
        "choices": [
            {
                "index": 0,
                "message": {"role": "assistant", "content": content},
                "finish_reason": "stop",
            }
        ],
        "usage": {"prompt_tokens": 0, "completion_tokens": 0, "total_tokens": 0},
    }

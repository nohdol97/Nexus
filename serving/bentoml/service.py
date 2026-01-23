from __future__ import annotations

import os
import bentoml
from bentoml.io import JSON


@bentoml.service(name="nexus_bentoml_worker", traffic={"timeout": 10})
class NexusBentoService:
    @bentoml.api(input=JSON(), output=JSON())
    def chat(self, payload: dict) -> dict:
        model = payload.get("model", "bentoml-mock")
        messages = payload.get("messages", [])
        user_text = ""
        for message in reversed(messages):
            if message.get("role") == "user":
                user_text = message.get("content", "")
                break

        content = f"bentoml response: {user_text}" if user_text else "bentoml response"
        return {
            "id": "bentoml-mock",
            "object": "chat.completion",
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

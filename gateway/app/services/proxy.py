from __future__ import annotations

import time
from typing import Any
from urllib.parse import urlparse

import httpx

from app.schemas import ChatCompletionRequest
from app.services.router import Upstream


class UpstreamError(Exception):
    pass


class ProxyClient:
    def __init__(self, timeout_seconds: float) -> None:
        self._client = httpx.AsyncClient(timeout=timeout_seconds)

    async def close(self) -> None:
        await self._client.aclose()

    async def forward(
        self,
        upstream: Upstream,
        path: str,
        payload: ChatCompletionRequest,
        headers: dict[str, str],
    ) -> dict[str, Any]:
        if self._is_mock(upstream.base_url):
            return self._mock_response(payload.model)
        url = upstream.base_url.rstrip("/") + path
        try:
            response = await self._client.post(url, json=payload.model_dump(), headers=headers)
        except httpx.HTTPError as exc:
            raise UpstreamError(str(exc)) from exc
        if response.status_code >= 500:
            raise UpstreamError(f"Upstream error: {response.status_code}")
        if response.status_code >= 400:
            raise UpstreamError(f"Upstream rejected request: {response.status_code}")
        return response.json()

    @staticmethod
    def _is_mock(url: str) -> bool:
        return urlparse(url).scheme == "mock"

    @staticmethod
    def _mock_response(model: str) -> dict[str, Any]:
        now = int(time.time())
        return {
            "id": f"mock-{now}",
            "object": "chat.completion",
            "created": now,
            "model": model,
            "choices": [
                {
                    "index": 0,
                    "message": {"role": "assistant", "content": "mock response"},
                    "finish_reason": "stop",
                }
            ],
            "usage": {"prompt_tokens": 0, "completion_tokens": 0, "total_tokens": 0},
        }

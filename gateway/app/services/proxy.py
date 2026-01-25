from __future__ import annotations

import time
from typing import Any
from urllib.parse import urlparse

import httpx
import grpc

from app.grpc import load_grpc_modules
from app.schemas import ChatCompletionRequest
from app.services.router import Upstream


class UpstreamError(Exception):
    pass


class ProxyClient:
    def __init__(self, timeout_seconds: float) -> None:
        self._client = httpx.AsyncClient(timeout=timeout_seconds)
        self._grpc_timeout = timeout_seconds
        self._grpc_channels: dict[str, grpc.aio.Channel] = {}
        self._grpc_stubs: dict[str, Any] = {}

    async def close(self) -> None:
        await self._client.aclose()
        for channel in self._grpc_channels.values():
            await channel.close()

    async def forward(
        self,
        upstream: Upstream,
        path: str,
        payload: ChatCompletionRequest,
        headers: dict[str, str],
    ) -> dict[str, Any]:
        if self._is_mock(upstream.base_url):
            if self._mock_should_fail(upstream.base_url):
                raise UpstreamError("Mock upstream failure")
            return self._mock_response(payload.model)
        if self._is_litellm(upstream.base_url):
            return await self._litellm_response(upstream.base_url, payload, headers)
        if self._is_grpc(upstream.base_url):
            return await self._grpc_response(upstream.base_url, payload, headers)
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

    @staticmethod
    def _mock_should_fail(url: str) -> bool:
        parsed = urlparse(url)
        return parsed.netloc == "fail" or parsed.path.strip("/") == "fail"

    @staticmethod
    def _is_litellm(url: str) -> bool:
        return urlparse(url).scheme == "litellm"

    @staticmethod
    def _is_grpc(url: str) -> bool:
        return urlparse(url).scheme == "grpc"

    @staticmethod
    def _grpc_target(url: str) -> str:
        parsed = urlparse(url)
        return parsed.netloc or parsed.path.strip("/")

    async def _grpc_response(
        self,
        url: str,
        payload: ChatCompletionRequest,
        headers: dict[str, str],
    ) -> dict[str, Any]:
        target = self._grpc_target(url)
        if not target:
            raise UpstreamError("Invalid gRPC upstream target")
        pb2, pb2_grpc = load_grpc_modules()
        stub = self._grpc_stubs.get(target)
        if stub is None:
            channel = grpc.aio.insecure_channel(target)
            stub = pb2_grpc.InferenceServiceStub(channel)
            self._grpc_channels[target] = channel
            self._grpc_stubs[target] = stub
        request = pb2.ChatCompletionRequest(
            request_id=headers.get("x-request-id", ""),
            trace_id=headers.get("x-trace-id", ""),
            idempotency_key=headers.get("idempotency-key", ""),
            model=payload.model,
            messages=[pb2.Message(role=msg.role, content=msg.content) for msg in payload.messages],
            metadata={
                "request_id": headers.get("x-request-id", ""),
                "trace_id": headers.get("x-trace-id", ""),
            },
        )
        try:
            response = await stub.ChatCompletion(request, timeout=self._grpc_timeout)
        except grpc.aio.AioRpcError as exc:
            raise UpstreamError(str(exc)) from exc

        now = int(time.time())
        return {
            "id": f"grpc-{response.request_id or now}",
            "object": "chat.completion",
            "created": now,
            "model": response.model or payload.model,
            "choices": [
                {
                    "index": 0,
                    "message": {"role": "assistant", "content": response.output},
                    "finish_reason": "stop",
                }
            ],
            "usage": {"prompt_tokens": 0, "completion_tokens": 0, "total_tokens": 0},
        }

    @staticmethod
    def _litellm_model(url: str, fallback: str) -> str:
        parsed = urlparse(url)
        model = parsed.netloc or parsed.path.strip("/")
        return model or fallback

    async def _litellm_response(
        self,
        url: str,
        payload: ChatCompletionRequest,
        headers: dict[str, str],
    ) -> dict[str, Any]:
        try:
            import litellm
        except ImportError as exc:
            raise UpstreamError("LiteLLM is not installed") from exc

        model = self._litellm_model(url, payload.model)
        try:
            response = await litellm.acompletion(
                model=model,
                messages=[message.model_dump() for message in payload.messages],
                temperature=payload.temperature,
                max_tokens=payload.max_tokens,
                metadata={"request_id": headers.get("x-request-id"), "trace_id": headers.get("x-trace-id")},
            )
        except Exception as exc:  # pragma: no cover - upstream library errors
            raise UpstreamError(str(exc)) from exc

        if hasattr(response, "model_dump"):
            return response.model_dump()
        if hasattr(response, "dict"):
            return response.dict()
        if isinstance(response, dict):
            return response
        return {"response": response}

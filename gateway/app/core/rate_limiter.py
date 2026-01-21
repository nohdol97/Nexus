from __future__ import annotations

import time
from collections import deque
from dataclasses import dataclass
from threading import Lock
from typing import Protocol

import redis.asyncio as redis


class RateLimitExceeded(Exception):
    pass


@dataclass
class RateLimitSnapshot:
    remaining: int
    reset_seconds: int


class RateLimitBackendError(Exception):
    pass


class RateLimiterBase(Protocol):
    async def check(self, key: str, limit_override: int | None = None) -> RateLimitSnapshot: ...

    async def close(self) -> None: ...


class RateLimiter:
    def __init__(self, max_requests: int, window_seconds: int) -> None:
        self._max_requests = max_requests
        self._window_seconds = window_seconds
        self._requests: dict[str, deque[float]] = {}
        self._lock = Lock()

    async def check(self, key: str, limit_override: int | None = None) -> RateLimitSnapshot:
        max_requests = limit_override or self._max_requests
        now = time.time()
        with self._lock:
            entries = self._requests.setdefault(key, deque())
            while entries and entries[0] <= now - self._window_seconds:
                entries.popleft()
            if len(entries) >= max_requests:
                reset_seconds = int(self._window_seconds - (now - entries[0])) if entries else 0
                raise RateLimitExceeded(
                    f"Rate limit exceeded. Retry in {reset_seconds} seconds."
                )
            entries.append(now)
            remaining = max_requests - len(entries)
            reset_seconds = int(self._window_seconds - (now - entries[0])) if entries else 0
            return RateLimitSnapshot(remaining=remaining, reset_seconds=reset_seconds)

    async def close(self) -> None:
        return None


class RedisRateLimiter:
    def __init__(self, redis_url: str, max_requests: int, window_seconds: int) -> None:
        self._redis = redis.from_url(redis_url, decode_responses=True)
        self._max_requests = max_requests
        self._window_seconds = window_seconds

    async def check(self, key: str, limit_override: int | None = None) -> RateLimitSnapshot:
        now = time.time()
        window = int(now // self._window_seconds)
        max_requests = limit_override or self._max_requests
        bucket_key = f"rate_limit:{key}:{max_requests}:{window}"
        try:
            pipe = self._redis.pipeline()
            pipe.incr(bucket_key)
            pipe.expire(bucket_key, self._window_seconds)
            count, _ = await pipe.execute()
        except Exception as exc:  # pragma: no cover - depends on redis availability
            raise RateLimitBackendError(str(exc)) from exc

        if count > max_requests:
            reset_seconds = int(self._window_seconds - (now % self._window_seconds))
            raise RateLimitExceeded(f"Rate limit exceeded. Retry in {reset_seconds} seconds.")

        remaining = max(0, max_requests - count)
        reset_seconds = int(self._window_seconds - (now % self._window_seconds))
        return RateLimitSnapshot(remaining=remaining, reset_seconds=reset_seconds)

    async def close(self) -> None:
        await self._redis.close()

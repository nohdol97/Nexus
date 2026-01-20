from __future__ import annotations

import time
from collections import deque
from dataclasses import dataclass
from threading import Lock


class RateLimitExceeded(Exception):
    pass


@dataclass
class RateLimitSnapshot:
    remaining: int
    reset_seconds: int


class RateLimiter:
    def __init__(self, max_requests: int, window_seconds: int) -> None:
        self._max_requests = max_requests
        self._window_seconds = window_seconds
        self._requests: dict[str, deque[float]] = {}
        self._lock = Lock()

    def check(self, key: str) -> RateLimitSnapshot:
        now = time.time()
        with self._lock:
            entries = self._requests.setdefault(key, deque())
            while entries and entries[0] <= now - self._window_seconds:
                entries.popleft()
            if len(entries) >= self._max_requests:
                reset_seconds = int(self._window_seconds - (now - entries[0])) if entries else 0
                raise RateLimitExceeded(
                    f"Rate limit exceeded. Retry in {reset_seconds} seconds."
                )
            entries.append(now)
            remaining = self._max_requests - len(entries)
            reset_seconds = int(self._window_seconds - (now - entries[0])) if entries else 0
            return RateLimitSnapshot(remaining=remaining, reset_seconds=reset_seconds)

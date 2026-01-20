from __future__ import annotations

import time
from dataclasses import dataclass
from enum import Enum


class CircuitState(str, Enum):
    CLOSED = "closed"
    OPEN = "open"
    HALF_OPEN = "half_open"


@dataclass
class CircuitSnapshot:
    state: CircuitState
    failure_count: int
    opened_seconds: int | None = None


class CircuitBreaker:
    def __init__(self, max_failures: int, reset_timeout_seconds: int) -> None:
        self._max_failures = max_failures
        self._reset_timeout_seconds = reset_timeout_seconds
        self._failure_count = 0
        self._state = CircuitState.CLOSED
        self._opened_at: float | None = None

    def allow_request(self) -> bool:
        if self._state == CircuitState.OPEN:
            if self._opened_at is None:
                return False
            if (time.time() - self._opened_at) >= self._reset_timeout_seconds:
                self._state = CircuitState.HALF_OPEN
                return True
            return False
        return True

    def record_success(self) -> None:
        self._failure_count = 0
        self._state = CircuitState.CLOSED
        self._opened_at = None

    def record_failure(self) -> None:
        if self._state == CircuitState.HALF_OPEN:
            self._state = CircuitState.OPEN
            self._opened_at = time.time()
            self._failure_count = self._max_failures
            return
        self._failure_count += 1
        if self._failure_count >= self._max_failures:
            self._state = CircuitState.OPEN
            self._opened_at = time.time()

    def snapshot(self) -> CircuitSnapshot:
        opened_seconds = None
        if self._state == CircuitState.OPEN and self._opened_at is not None:
            opened_seconds = int(time.time() - self._opened_at)
        return CircuitSnapshot(
            state=self._state,
            failure_count=self._failure_count,
            opened_seconds=opened_seconds,
        )

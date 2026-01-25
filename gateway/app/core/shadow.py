from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class ShadowPolicy:
    enabled: bool
    percent: int
    target: str

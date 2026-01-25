from __future__ import annotations

from dataclasses import dataclass
import hashlib


@dataclass(frozen=True)
class ShadowPolicy:
    enabled: bool
    percent: int
    target: str


def should_shadow(request_id: str | None, percent: int) -> bool:
    if percent <= 0:
        return False
    if percent >= 100:
        return True
    if not request_id:
        return False
    digest = hashlib.sha256(request_id.encode("utf-8")).hexdigest()
    bucket = int(digest, 16) % 100
    return bucket < percent

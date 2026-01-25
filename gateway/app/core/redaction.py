from __future__ import annotations

import hashlib

from app.core.config import settings


def mask_ip(value: str | None) -> str | None:
    if not value:
        return None
    if not settings.pii_masking_enabled:
        return value
    if ":" in value:
        parts = value.split(":")
        if len(parts) <= 2:
            return value
        return ":".join(parts[:2] + ["*"] * (len(parts) - 2))
    parts = value.split(".")
    if len(parts) != 4:
        return value
    parts[-1] = "0"
    return ".".join(parts)


def hash_identifier(value: str | None) -> str | None:
    if not value:
        return None
    if not settings.pii_masking_enabled:
        return value
    salt = settings.pii_hash_salt or ""
    digest = hashlib.sha256(f"{salt}:{value}".encode("utf-8")).hexdigest()
    return digest[:16]

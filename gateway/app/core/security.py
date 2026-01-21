from __future__ import annotations

from dataclasses import dataclass
from typing import Any

import jwt
from fastapi import Header, HTTPException, status

from app.core.config import settings


def _parse_bearer(authorization: str | None) -> str | None:
    if not authorization:
        return None
    parts = authorization.split()
    if len(parts) != 2 or parts[0].lower() != "bearer":
        return None
    return parts[1].strip()


@dataclass
class AuthContext:
    principal: str
    method: str
    allowed_models: set[str] | None = None
    rate_limit_per_minute: int | None = None

    @property
    def rate_limit_key(self) -> str:
        return self.principal


def _load_api_key_policy(key: str) -> dict[str, Any]:
    policy_map = settings.api_key_policy_map()
    policy = policy_map.get(key)
    if policy is None:
        return {}
    if not isinstance(policy, dict):
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Invalid API key policy format",
        )
    return policy


def _auth_from_api_key(key: str) -> AuthContext:
    policy = _load_api_key_policy(key)
    allowed_models = None
    models = policy.get("allowed_models")
    if isinstance(models, list):
        allowed_models = {str(model) for model in models}
    rate_limit_override = policy.get("rate_limit_per_minute")
    if isinstance(rate_limit_override, (int, float)):
        rate_limit_override = int(rate_limit_override)
    else:
        rate_limit_override = None
    return AuthContext(
        principal=key,
        method="api_key",
        allowed_models=allowed_models,
        rate_limit_per_minute=rate_limit_override,
    )


def _decode_jwt(token: str) -> dict[str, Any]:
    key = settings.jwt_public_key or settings.jwt_secret
    if not key:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="JWT validation is not configured",
        )
    options = {"verify_aud": bool(settings.jwt_audience)}
    try:
        return jwt.decode(
            token,
            key=key,
            algorithms=settings.jwt_algorithms_list(),
            issuer=settings.jwt_issuer,
            audience=settings.jwt_audience,
            options=options,
        )
    except jwt.PyJWTError as exc:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid JWT",
        ) from exc


def _auth_from_jwt(token: str) -> AuthContext:
    claims = _decode_jwt(token)
    principal = str(claims.get("sub") or "jwt")
    models = claims.get("models") or claims.get("allowed_models")
    allowed_models = None
    if isinstance(models, list):
        allowed_models = {str(model) for model in models}
    rate_limit_override = claims.get("rate_limit_per_minute")
    if isinstance(rate_limit_override, (int, float)):
        rate_limit_override = int(rate_limit_override)
    else:
        rate_limit_override = None
    return AuthContext(
        principal=principal,
        method="jwt",
        allowed_models=allowed_models,
        rate_limit_per_minute=rate_limit_override,
    )


def require_auth(
    x_api_key: str | None = Header(default=None, alias="X-API-Key"),
    authorization: str | None = Header(default=None, alias="Authorization"),
) -> AuthContext:
    bearer = _parse_bearer(authorization)
    if bearer and (settings.jwt_secret or settings.jwt_public_key):
        return _auth_from_jwt(bearer)

    key = x_api_key or bearer
    if not key:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Missing API key or JWT",
        )

    policy_map = settings.api_key_policy_map()
    if key not in settings.api_keys and key not in policy_map:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Invalid API key",
        )

    return _auth_from_api_key(key)

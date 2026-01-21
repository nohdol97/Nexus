from __future__ import annotations

import json
from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_prefix="GATEWAY_", case_sensitive=False)

    api_keys: str = "dev-key"
    rate_limit_per_minute: int = 60
    rate_limit_window_seconds: int = 60
    circuit_breaker_max_failures: int = 5
    circuit_breaker_reset_seconds: int = 30
    request_timeout_seconds: float = 10.0
    upstreams: str = ""
    default_upstream: str | None = None
    fallbacks: str = ""
    redis_url: str | None = None
    api_key_policies: str = ""
    route_policies: str = ""
    jwt_secret: str | None = None
    jwt_public_key: str | None = None
    jwt_algorithms: str = "HS256"
    jwt_issuer: str | None = None
    jwt_audience: str | None = None

    def api_key_set(self) -> set[str]:
        if not self.api_keys:
            return set()
        cleaned = self.api_keys.strip()
        if not cleaned:
            return set()
        if cleaned.startswith("["):
            try:
                parsed = json.loads(cleaned)
            except json.JSONDecodeError:
                parsed = None
            else:
                if isinstance(parsed, list):
                    return {str(item).strip() for item in parsed if str(item).strip()}
        parts = [part.strip() for part in cleaned.replace(";", ",").split(",") if part.strip()]
        return set(parts)

    def upstream_map(self) -> dict[str, str]:
        if not self.upstreams:
            return {}
        items: dict[str, str] = {}
        raw_entries = [entry.strip() for entry in self.upstreams.replace(",", ";").split(";")]
        for entry in raw_entries:
            if not entry:
                continue
            if "=" not in entry:
                raise ValueError(f"Invalid upstream entry: {entry}")
            name, url = entry.split("=", 1)
            items[name.strip()] = url.strip()
        return items

    def fallback_map(self) -> dict[str, list[str]]:
        if not self.fallbacks:
            return {}
        mapping: dict[str, list[str]] = {}
        raw_entries = [entry.strip() for entry in self.fallbacks.split(";")]
        for entry in raw_entries:
            if not entry:
                continue
            if "=" not in entry:
                raise ValueError(f"Invalid fallback entry: {entry}")
            name, values = entry.split("=", 1)
            fallbacks = [value.strip() for value in values.split(",") if value.strip()]
            mapping[name.strip()] = fallbacks
        return mapping

    def api_key_policy_map(self) -> dict[str, dict[str, object]]:
        if not self.api_key_policies:
            return {}
        try:
            data = json.loads(self.api_key_policies)
        except json.JSONDecodeError as exc:
            raise ValueError("Invalid API key policies JSON") from exc
        if not isinstance(data, dict):
            raise ValueError("API key policies must be a JSON object")
        return data

    def route_policy_map(self) -> dict[str, dict[str, object]]:
        if not self.route_policies:
            return {}
        try:
            data = json.loads(self.route_policies)
        except json.JSONDecodeError as exc:
            raise ValueError("Invalid route policies JSON") from exc
        if not isinstance(data, dict):
            raise ValueError("Route policies must be a JSON object")
        return data

    def jwt_algorithms_list(self) -> list[str]:
        return [algo.strip() for algo in self.jwt_algorithms.split(",") if algo.strip()]


settings = Settings()

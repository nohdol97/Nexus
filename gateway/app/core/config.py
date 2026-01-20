from __future__ import annotations

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


def _default_api_keys() -> set[str]:
    return {"dev-key"}


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_prefix="GATEWAY_", case_sensitive=False)

    api_keys: set[str] = Field(default_factory=_default_api_keys)
    rate_limit_per_minute: int = 60
    rate_limit_window_seconds: int = 60
    circuit_breaker_max_failures: int = 5
    circuit_breaker_reset_seconds: int = 30
    request_timeout_seconds: float = 10.0
    upstreams: str = ""
    default_upstream: str | None = None
    fallbacks: str = ""
    redis_url: str | None = None

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


settings = Settings()

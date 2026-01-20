from __future__ import annotations

from dataclasses import dataclass

from app.core.config import settings


@dataclass(frozen=True)
class Upstream:
    name: str
    base_url: str


class RouteSelector:
    def __init__(self) -> None:
        self._upstreams = self._load_upstreams()

    @staticmethod
    def _load_upstreams() -> dict[str, Upstream]:
        mapping = settings.upstream_map()
        return {name: Upstream(name=name, base_url=url) for name, url in mapping.items()}

    def select(self, model: str) -> Upstream | None:
        if model in self._upstreams:
            return self._upstreams[model]
        if settings.default_upstream and settings.default_upstream in self._upstreams:
            return self._upstreams[settings.default_upstream]
        return None

    def all(self) -> list[Upstream]:
        return list(self._upstreams.values())

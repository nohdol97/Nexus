from __future__ import annotations

from dataclasses import dataclass
import hashlib
import random

from app.core.config import settings


@dataclass(frozen=True)
class Upstream:
    name: str
    base_url: str


@dataclass(frozen=True)
class RouteTarget:
    name: str
    weight: int


@dataclass(frozen=True)
class RoutePolicy:
    strategy: str
    targets: list[RouteTarget]


class RouteSelector:
    def __init__(self) -> None:
        self._upstreams = self._load_upstreams()
        self._policies = self._load_policies()

    @staticmethod
    def _load_upstreams() -> dict[str, Upstream]:
        mapping = settings.upstream_map()
        return {name: Upstream(name=name, base_url=url) for name, url in mapping.items()}

    @staticmethod
    def _load_policies() -> dict[str, RoutePolicy]:
        policies: dict[str, RoutePolicy] = {}
        raw_policies = settings.route_policy_map()
        for model, raw in raw_policies.items():
            policies[model] = RouteSelector._parse_policy(model, raw)
        return policies

    @staticmethod
    def _parse_policy(model: str, raw: object) -> RoutePolicy:
        if not isinstance(raw, dict):
            raise ValueError(f"Route policy for {model} must be an object")
        strategy = str(raw.get("strategy", "weighted"))
        if strategy == "weighted":
            targets_raw = raw.get("targets")
            if not isinstance(targets_raw, list) or not targets_raw:
                raise ValueError(f"Route policy for {model} requires targets list")
            targets = [
                RouteTarget(name=str(item["name"]), weight=int(item.get("weight", 1)))
                for item in targets_raw
                if isinstance(item, dict) and "name" in item
            ]
        elif strategy == "canary":
            primary = raw.get("primary")
            canary = raw.get("canary")
            percent = int(raw.get("percent", raw.get("percentage", 5)))
            if not primary or not canary:
                raise ValueError(f"Route policy for {model} requires primary/canary")
            percent = max(0, min(100, percent))
            targets = [
                RouteTarget(name=str(primary), weight=max(0, 100 - percent)),
                RouteTarget(name=str(canary), weight=percent),
            ]
        elif strategy == "direct":
            target = raw.get("target")
            if not target:
                raise ValueError(f"Route policy for {model} requires target")
            targets = [RouteTarget(name=str(target), weight=100)]
        else:
            raise ValueError(f"Unsupported route policy strategy: {strategy}")

        targets = [target for target in targets if target.weight > 0]
        if not targets:
            raise ValueError(f"Route policy for {model} has no valid targets")
        return RoutePolicy(strategy=strategy, targets=targets)

    @staticmethod
    def _pick_target(targets: list[RouteTarget], request_id: str | None) -> RouteTarget:
        total = sum(target.weight for target in targets)
        if total <= 0:
            return targets[0]
        if request_id:
            digest = hashlib.sha256(request_id.encode("utf-8")).hexdigest()
            choice = int(digest, 16) % total
        else:
            choice = random.randint(0, total - 1)
        cumulative = 0
        for target in targets:
            cumulative += target.weight
            if choice < cumulative:
                return target
        return targets[-1]

    def select(self, model: str, request_id: str | None = None) -> Upstream | None:
        policy = self._policies.get(model)
        if policy:
            target = self._pick_target(policy.targets, request_id)
            if target.name in self._upstreams:
                return self._upstreams[target.name]
        if model in self._upstreams:
            return self._upstreams[model]
        if settings.default_upstream and settings.default_upstream in self._upstreams:
            return self._upstreams[settings.default_upstream]
        return None
        if model in self._upstreams:
            return self._upstreams[model]
        if settings.default_upstream and settings.default_upstream in self._upstreams:
            return self._upstreams[settings.default_upstream]
        return None

    def all(self) -> list[Upstream]:
        return list(self._upstreams.values())

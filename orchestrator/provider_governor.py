from __future__ import annotations

from dataclasses import dataclass, field
from time import monotonic


@dataclass
class ProviderHealth:
    failures: int = 0
    cooldown_until: float = 0.0
    latency_ms: float | None = None
    quality_score: float = 1.0


@dataclass
class ProviderGovernor:
    failure_threshold: int = 3
    cooldown_seconds: int = 60
    health: dict[str, ProviderHealth] = field(default_factory=dict)

    def available(self, provider: str) -> bool:
        state = self.health.setdefault(provider, ProviderHealth())
        return monotonic() >= state.cooldown_until

    def record_success(self, provider: str, latency_ms: float, quality_score: float = 1.0) -> None:
        state = self.health.setdefault(provider, ProviderHealth())
        state.failures = 0
        state.latency_ms = latency_ms
        state.quality_score = quality_score

    def record_failure(self, provider: str) -> None:
        state = self.health.setdefault(provider, ProviderHealth())
        state.failures += 1
        if state.failures >= self.failure_threshold:
            state.cooldown_until = monotonic() + self.cooldown_seconds

    def rank(self, providers: list[str]) -> list[str]:
        eligible = [p for p in providers if self.available(p)]
        return sorted(eligible, key=lambda p: self.health.setdefault(p, ProviderHealth()).quality_score, reverse=True)

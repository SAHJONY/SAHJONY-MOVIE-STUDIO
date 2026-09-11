from __future__ import annotations

from dataclasses import dataclass, field
from time import monotonic


FATAL_PROVIDER_REASONS = {"auth_invalid", "plan_ineligible", "provider_disabled"}


@dataclass
class ProviderHealth:
    failures: int = 0
    cooldown_until: float = 0.0
    latency_ms: float | None = None
    quality_score: float = 1.0
    blocked: bool = False
    block_reason: str | None = None


@dataclass
class ProviderGovernor:
    failure_threshold: int = 3
    cooldown_seconds: int = 60
    health: dict[str, ProviderHealth] = field(default_factory=dict)

    def available(self, provider: str) -> bool:
        state = self.health.setdefault(provider, ProviderHealth())
        return not state.blocked and monotonic() >= state.cooldown_until

    def record_success(self, provider: str, latency_ms: float, quality_score: float = 1.0) -> None:
        state = self.health.setdefault(provider, ProviderHealth())
        state.failures = 0
        state.cooldown_until = 0.0
        state.latency_ms = latency_ms
        state.quality_score = quality_score
        state.blocked = False
        state.block_reason = None
    def record_failure(self, provider: str, reason: str = "transient") -> None:
        state = self.health.setdefault(provider, ProviderHealth())
        state.failures += 1
        state.block_reason = reason
        if reason in FATAL_PROVIDER_REASONS:
            state.blocked = True
            return
        if state.failures >= self.failure_threshold:
            state.cooldown_until = monotonic() + self.cooldown_seconds

    def unblock(self, provider: str) -> None:
        state = self.health.setdefault(provider, ProviderHealth())
        state.blocked = False
        state.block_reason = None
        state.failures = 0
        state.cooldown_until = 0.0

    def rank(self, providers: list[str]) -> list[str]:
        eligible = [p for p in providers if self.available(p)]
        return sorted(
            eligible,
            key=lambda p: self.health.setdefault(p, ProviderHealth()).quality_score,
            reverse=True,
        )

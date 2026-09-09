from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from .providers.higgsfield import HiggsfieldRouter


@dataclass(frozen=True)
class ProviderCandidate:
    provider: str
    model: str
    tier: str
    estimated_credits_5s_720p: float


class ProviderRegistry:
    """Deterministic provider/model routing with an explicit fallback chain."""

    def __init__(self) -> None:
        self.higgsfield = HiggsfieldRouter()

    def candidates(self, shot_spec: dict[str, Any], attempt: int) -> list[ProviderCandidate]:
        priority = shot_spec.get("priority", "normal")
        if priority == "hero" or attempt > 1:
            return [
                ProviderCandidate("higgsfield", "cinematic_studio_3_0", "final", 25.0),
                ProviderCandidate("higgsfield", "seedance_2_0_mini", "fallback", 12.5),
            ]
        return [
            ProviderCandidate("higgsfield", "seedance_2_0_mini", "draft", 12.5),
            ProviderCandidate("higgsfield", "cinematic_studio_3_0", "fallback", 25.0),
        ]

from __future__ import annotations

from dataclasses import dataclass, field


@dataclass(frozen=True)
class ModelCapability:
    provider: str
    model: str
    modalities: frozenset[str]
    strengths: frozenset[str] = field(default_factory=frozenset)
    max_duration_s: int | None = None
    supports_references: bool = False
    supports_audio: bool = False
    cost_rank: int = 2
    quality_rank: int = 2


class CapabilityRegistry:
    def __init__(self) -> None:
        self.models: list[ModelCapability] = []

    def register(self, capability: ModelCapability) -> None:
        self.models.append(capability)

    def match(self, *, modality: str, needs: set[str] | None = None) -> list[ModelCapability]:
        needs = needs or set()
        matches = [m for m in self.models if modality in m.modalities and needs <= set(m.strengths)]
        return sorted(matches, key=lambda m: (-m.quality_rank, m.cost_rank))

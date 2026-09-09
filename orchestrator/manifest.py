from __future__ import annotations

from dataclasses import dataclass, field, asdict
from typing import Any


@dataclass
class ShotManifest:
    shot_id: str
    description: str
    duration_seconds: int
    priority: str = "normal"
    camera: dict[str, Any] = field(default_factory=dict)
    lighting: dict[str, Any] = field(default_factory=dict)
    performance: dict[str, Any] = field(default_factory=dict)
    continuity: dict[str, Any] = field(default_factory=dict)


@dataclass
class ProductionManifest:
    project_title: str
    concept: str
    style_bible: dict[str, Any]
    character_bible: dict[str, Any]
    shots: list[ShotManifest]

    def as_dict(self) -> dict[str, Any]:
        return asdict(self)

    @property
    def duration_seconds(self) -> int:
        return sum(s.duration_seconds for s in self.shots)

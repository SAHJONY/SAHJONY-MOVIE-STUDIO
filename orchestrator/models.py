from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass(frozen=True)
class CameraSpec:
    shot_size: str = "medium"
    lens_mm: int = 50
    movement: str = "locked"
    height_m: float = 1.5
    aperture: float = 2.8
    command: dict[str, Any] = field(default_factory=dict)


@dataclass(frozen=True)
class LightingSpec:
    key: str = "motivated_soft_key"
    fill_ratio: float = 0.35
    rim: str | None = None
    mood: str = "cinematic"


@dataclass(frozen=True)
class ShotSpec:
    shot_id: str
    description: str
    duration_seconds: int = 5
    aspect_ratio: str = "16:9"
    camera: CameraSpec = field(default_factory=CameraSpec)
    lighting: LightingSpec = field(default_factory=LightingSpec)
    performance: dict[str, Any] = field(default_factory=dict)
    continuity: dict[str, Any] = field(default_factory=dict)
    style: dict[str, Any] = field(default_factory=dict)
    references: list[dict[str, str]] = field(default_factory=list)
    audio: dict[str, Any] = field(default_factory=dict)
    spatial: dict[str, Any] = field(default_factory=dict)
    priority: str = "normal"


@dataclass(frozen=True)
class GenerationRequest:
    provider: str
    model: str
    prompt: str
    duration: int
    aspect_ratio: str
    params: dict[str, Any] = field(default_factory=dict)
    medias: list[dict[str, str]] = field(default_factory=list)


@dataclass(frozen=True)
class GenerationResult:
    provider_job_id: str
    output_uri: str
    provider: str
    model: str
    cost_credits: float | None = None
    metadata: dict[str, Any] = field(default_factory=dict)

from __future__ import annotations

from dataclasses import asdict
from typing import Any

from .models import CameraSpec, LightingSpec, ShotSpec


class MasterDirector:
    """Deterministic first-pass planner that emits canonical shot state."""

    def plan_shot(self, brief: dict[str, Any], shot_id: str) -> dict[str, Any]:
        duration = int(brief.get("duration_seconds", 5))
        duration = max(3, min(duration, 15))

        camera = CameraSpec(
            shot_size=brief.get("shot_size", "medium"),
            lens_mm=int(brief.get("lens_mm", 50)),
            movement=brief.get("camera_movement", "slow_dolly_in"),
            height_m=float(brief.get("camera_height_m", 1.5)),
            aperture=float(brief.get("aperture", 2.8)),
        )
        lighting = LightingSpec(
            key=brief.get("key_light", "motivated_soft_key"),
            fill_ratio=float(brief.get("fill_ratio", 0.35)),
            rim=brief.get("rim_light"),
            mood=brief.get("lighting_mood", "cinematic"),
        )
        spec = ShotSpec(
            shot_id=shot_id,
            description=brief["description"],
            duration_seconds=duration,
            aspect_ratio=brief.get("aspect_ratio", "16:9"),
            camera=camera,
            lighting=lighting,
            performance=brief.get("performance", {}),
            continuity=brief.get("continuity", {}),
            style=brief.get("style", {}),
            references=brief.get("references", []),
            audio=brief.get("audio", {}),
            priority=brief.get("priority", "normal"),
        )
        return asdict(spec)

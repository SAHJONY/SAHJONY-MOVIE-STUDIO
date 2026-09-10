from __future__ import annotations

from dataclasses import asdict
from typing import Any

from .cinematography import CameraCommand
from .models import CameraSpec, LightingSpec, ShotSpec


MOVEMENT_ALIASES = {
    "slow_dolly_in": "dolly_in",
    "slow_dolly_out": "dolly_out",
    "static": "locked",
    "track": "follow",
}


class MasterDirector:
    """Deterministic planner that emits canonical, executable shot state."""

    def plan_shot(self, brief: dict[str, Any], shot_id: str) -> dict[str, Any]:
        duration = max(3, min(int(brief.get("duration_seconds", 5)), 15))
        movement = brief.get("camera_movement", "dolly_in")
        verb = MOVEMENT_ALIASES.get(movement, movement)
        command = CameraCommand(
            verb=verb,
            subject=brief.get("camera_subject"),
            lens_mm=int(brief.get("lens_mm", 50)),
            duration_s=duration,
            easing=brief.get("camera_easing", "cinematic"),
            radius_m=brief.get("orbit_radius_m"),
            degrees=brief.get("orbit_degrees"),
            distance_m=brief.get("camera_distance_m"),
            height_m=float(brief.get("camera_height_m", 1.5)),
            maintain_screen_direction=bool(brief.get("maintain_screen_direction", True)),
            maintain_eyeline=bool(brief.get("maintain_eyeline", True)),
        )
        command.validate()
        camera = CameraSpec(
            shot_size=brief.get("shot_size", "medium"),
            lens_mm=command.lens_mm,
            movement=movement,
            height_m=command.height_m,
            aperture=float(brief.get("aperture", 2.8)),
            command=asdict(command),
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
            spatial=brief.get("spatial", {}),
            priority=brief.get("priority", "normal"),
        )
        return asdict(spec)

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class ShotGeometry:
    subject_distance_m: float = 3.0
    camera_height_m: float = 1.5
    subject_height_m: float = 1.7
    screen_direction: str | None = None
    eyeline_axis: str | None = None

    def validate(self) -> None:
        if self.subject_distance_m <= 0:
            raise ValueError("subject_distance_m must be positive")
        if self.camera_height_m < 0:
            raise ValueError("camera_height_m cannot be negative")
        if self.subject_height_m <= 0:
            raise ValueError("subject_height_m must be positive")

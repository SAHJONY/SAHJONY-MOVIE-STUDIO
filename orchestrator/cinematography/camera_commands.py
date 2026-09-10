from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class CameraCommand:
    verb: str = "locked"
    subject: str | None = None
    lens_mm: int = 50
    duration_s: float = 5.0
    easing: str = "cinematic"
    radius_m: float | None = None
    degrees: float | None = None
    distance_m: float | None = None
    height_m: float = 1.5
    maintain_screen_direction: bool = True
    maintain_eyeline: bool = True
    interruptible: bool = True

    def validate(self) -> None:
        allowed = {"locked", "dolly_in", "dolly_out", "orbit", "truck", "pedestal", "crane", "follow", "handheld", "flythrough"}
        if self.verb not in allowed:
            raise ValueError(f"Unsupported camera verb: {self.verb}")
        if not 8 <= self.lens_mm <= 300:
            raise ValueError("lens_mm outside supported range")
        if self.duration_s <= 0:
            raise ValueError("duration_s must be positive")

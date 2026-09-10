from __future__ import annotations

from dataclasses import dataclass


@dataclass
class CameraState:
    subject: str | None = None
    lens_mm: int = 50
    height_m: float = 1.5
    heading_deg: float = 0.0
    pitch_deg: float = 0.0
    roll_deg: float = 0.0
    screen_direction: str | None = None
    eyeline_axis: str | None = None
    active_command_id: str | None = None

    def snapshot(self) -> dict:
        return {
            "subject": self.subject,
            "lens_mm": self.lens_mm,
            "height_m": self.height_m,
            "heading_deg": self.heading_deg,
            "pitch_deg": self.pitch_deg,
            "roll_deg": self.roll_deg,
            "screen_direction": self.screen_direction,
            "eyeline_axis": self.eyeline_axis,
        }

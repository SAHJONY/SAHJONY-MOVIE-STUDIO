from __future__ import annotations

from dataclasses import dataclass

from .camera_commands import CameraCommand


@dataclass(frozen=True)
class ContinuityCheck:
    ok: bool
    issues: tuple[str, ...] = ()


def check_camera_continuity(previous: dict, incoming: CameraCommand) -> ContinuityCheck:
    issues: list[str] = []
    prev_direction = previous.get("screen_direction")
    next_direction = previous.get("next_screen_direction", prev_direction)
    if incoming.maintain_screen_direction and prev_direction and next_direction != prev_direction:
        issues.append("screen_direction_break")
    prev_axis = previous.get("eyeline_axis")
    next_axis = previous.get("next_eyeline_axis", prev_axis)
    if incoming.maintain_eyeline and prev_axis and next_axis != prev_axis:
        issues.append("eyeline_break")
    return ContinuityCheck(not issues, tuple(issues))

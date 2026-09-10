from __future__ import annotations

from dataclasses import dataclass

from .camera_commands import CameraCommand


@dataclass(frozen=True)
class HandoffDecision:
    action: str
    reason: str


def resolve_handoff(active: CameraCommand | None, incoming: CameraCommand) -> HandoffDecision:
    incoming.validate()
    if active is None:
        return HandoffDecision("start", "no_active_command")
    if not active.interruptible:
        return HandoffDecision("queue", "active_command_locked")
    if active.subject and incoming.subject and active.subject != incoming.subject:
        return HandoffDecision("cut", "subject_changed")
    if active.verb == incoming.verb and active.subject == incoming.subject:
        return HandoffDecision("blend", "compatible_motion")
    return HandoffDecision("interrupt", "director_override")

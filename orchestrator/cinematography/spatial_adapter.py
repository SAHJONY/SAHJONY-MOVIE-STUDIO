from __future__ import annotations

from typing import Protocol

from .camera_commands import CameraCommand
from .camera_state import CameraState


class SpatialAdapter(Protocol):
    def apply_camera(self, command: CameraCommand, state: CameraState) -> CameraState: ...


class NullSpatialAdapter:
    """Deterministic adapter for planning/tests before Unreal/Blender/Cesium execution."""

    def apply_camera(self, command: CameraCommand, state: CameraState) -> CameraState:
        command.validate()
        state.subject = command.subject or state.subject
        state.lens_mm = command.lens_mm
        state.height_m = command.height_m
        return state

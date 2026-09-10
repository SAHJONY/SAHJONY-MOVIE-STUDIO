from __future__ import annotations

PHASES = (
    "IDEA", "DEVELOPMENT", "SCRIPT_LOCK", "VISDEV", "STORYBOARD", "PREVIS",
    "ASSET_BUILD", "SHOT_READY", "RENDERING", "QA", "EDIT", "FINAL",
)

SHOT_STATES = (
    "PLANNED", "SPECIFIED", "ASSETS_READY", "GENERATING", "QA_PENDING",
    "REJECTED", "APPROVED", "LOCKED",
)


def advance_phase(current: str, target: str) -> str:
    if current not in PHASES or target not in PHASES:
        raise ValueError("unknown phase")
    if PHASES.index(target) < PHASES.index(current):
        raise ValueError("phase rollback requires explicit revision workflow")
    return target


def transition_shot(current: str, target: str) -> str:
    allowed = {
        "PLANNED": {"SPECIFIED"},
        "SPECIFIED": {"ASSETS_READY"},
        "ASSETS_READY": {"GENERATING"},
        "GENERATING": {"QA_PENDING"},
        "QA_PENDING": {"APPROVED", "REJECTED"},
        "REJECTED": {"GENERATING"},
        "APPROVED": {"LOCKED", "REJECTED"},
        "LOCKED": set(),
    }
    if target not in allowed.get(current, set()):
        raise ValueError(f"invalid shot transition: {current} -> {target}")
    return target

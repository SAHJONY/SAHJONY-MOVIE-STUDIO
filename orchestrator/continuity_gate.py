from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from .identity_engine import CharacterIdentityEngine, IdentityPack


@dataclass(frozen=True)
class ContinuityDecision:
    passed: bool
    violations: tuple[str, ...]
    required_patch: dict[str, Any]


class ContinuityGate:
    """Hard pre-render gate for identity, wardrobe, props, weather and screen direction."""

    def __init__(self) -> None:
        self.identity = CharacterIdentityEngine()

    def evaluate(self, shot_spec: dict[str, Any], identity_pack: IdentityPack,
                 required_world: dict[str, Any]) -> ContinuityDecision:
        violations: list[str] = []
        patch: dict[str, Any] = {}
        identity = self.identity.validate_shot_spec(shot_spec, identity_pack)
        violations.extend(identity.violations)
        continuity = shot_spec.get("continuity", {})
        for key, expected in required_world.items():
            actual = continuity.get(key)
            if actual != expected:
                violations.append(f"{key} continuity drift")
                patch.setdefault("continuity", {})[key] = expected
        return ContinuityDecision(not violations, tuple(violations), patch)

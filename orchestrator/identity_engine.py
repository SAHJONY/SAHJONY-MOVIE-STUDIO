from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass(frozen=True)
class IdentityPack:
    character_id: str
    canonical_id: str
    immutable_traits: dict[str, Any] = field(default_factory=dict)
    appearance_profile: dict[str, Any] = field(default_factory=dict)
    wardrobe_profile: dict[str, Any] = field(default_factory=dict)
    performance_profile: dict[str, Any] = field(default_factory=dict)
    negative_constraints: tuple[str, ...] = ()
    identity_threshold: float = 0.95


@dataclass(frozen=True)
class IdentityCheck:
    passed: bool
    score: float
    violations: tuple[str, ...] = ()


class CharacterIdentityEngine:
    """Enforces immutable character identity before and after generation."""

    def required_context(self, pack: IdentityPack) -> dict[str, Any]:
        return {
            "canonical_id": pack.canonical_id,
            "immutable_traits": pack.immutable_traits,
            "appearance_profile": pack.appearance_profile,
            "wardrobe_profile": pack.wardrobe_profile,
            "performance_profile": pack.performance_profile,
            "negative_constraints": list(pack.negative_constraints),
        }

    def validate_shot_spec(self, shot_spec: dict[str, Any], pack: IdentityPack) -> IdentityCheck:
        continuity = shot_spec.get("continuity", {})
        violations: list[str] = []
        if continuity.get("character_id") not in {None, pack.canonical_id}:
            violations.append("character_id drift")
        wardrobe = continuity.get("wardrobe")
        if wardrobe and pack.wardrobe_profile:
            expected = ", ".join(str(v) for v in pack.wardrobe_profile.values())
            if expected and any(str(v) not in wardrobe for v in pack.wardrobe_profile.values()):
                violations.append("wardrobe drift")
        return IdentityCheck(not violations, 1.0 if not violations else 0.0, tuple(violations))

    def evaluate_render(self, score: float, violations: list[str], pack: IdentityPack) -> IdentityCheck:
        normalized = max(0.0, min(float(score), 1.0))
        passed = normalized >= pack.identity_threshold and not violations
        return IdentityCheck(passed, normalized, tuple(violations))

    def apply_acceptance_gate(self, shot_spec: dict[str, Any], pack: IdentityPack) -> dict[str, Any]:
        patched = dict(shot_spec)
        criteria = dict(patched.get("acceptance_criteria", {}))
        criteria["identity_min"] = pack.identity_threshold
        patched["acceptance_criteria"] = criteria
        patched["identity_context"] = self.required_context(pack)
        return patched

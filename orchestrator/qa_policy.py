from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class AcceptancePolicy:
    identity_min: float = 0.95
    continuity_min: float = 0.90
    artifact_min: float = 0.90
    physics_min: float = 0.85
    av_sync_min: float = 0.85

    def passes(self, scores: dict[str, float]) -> bool:
        return (
            scores.get("identity", 0.0) >= self.identity_min
            and scores.get("continuity", 0.0) >= self.continuity_min
            and scores.get("artifacts", 0.0) >= self.artifact_min
            and scores.get("physics", 0.0) >= self.physics_min
            and scores.get("av_sync", 1.0) >= self.av_sync_min
        )

    def remediation(self, scores: dict[str, float]) -> dict:
        patch: dict = {"qa_remediation": []}
        if scores.get("identity", 0.0) < self.identity_min:
            patch["qa_remediation"].append("increase character/reference conditioning")
        if scores.get("continuity", 0.0) < self.continuity_min:
            patch["qa_remediation"].append("reassert wardrobe, props, geography, and screen direction")
        if scores.get("artifacts", 0.0) < self.artifact_min:
            patch["qa_remediation"].append("reduce complex motion and explicitly forbid observed artifacts")
        if scores.get("physics", 0.0) < self.physics_min:
            patch["qa_remediation"].append("simplify physical interaction and clarify contacts/trajectories")
        if scores.get("av_sync", 1.0) < self.av_sync_min:
            patch["qa_remediation"].append("regenerate or post-sync dialogue/audio")
        return patch

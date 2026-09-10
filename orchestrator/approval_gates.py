from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class ApprovalGate:
    name: str
    required_for: tuple[str, ...]
    automatic_if: dict[str, float]


GATES = {
    "script_lock": ApprovalGate("script_lock", ("SCRIPT_LOCK",), {"continuity": .95}),
    "hero_asset": ApprovalGate("hero_asset", ("hero_character", "hero_environment"), {"identity": .97, "style": .95}),
    "shot_lock": ApprovalGate("shot_lock", ("LOCKED",), {"identity": .95, "continuity": .90, "artifacts": .90}),
    "final_master": ApprovalGate("final_master", ("FINAL",), {"av_sync": .95, "continuity": .95}),
}


def evaluate_gate(name: str, metrics: dict[str, float]) -> bool:
    gate = GATES[name]
    return all(metrics.get(metric, 0.0) >= threshold for metric, threshold in gate.automatic_if.items())

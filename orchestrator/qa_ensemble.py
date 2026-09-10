from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class QAScore:
    identity: float
    continuity: float
    artifacts: float
    physics: float
    av_sync: float

    @property
    def overall(self) -> float:
        weights = (0.30, 0.25, 0.20, 0.15, 0.10)
        values = (self.identity, self.continuity, self.artifacts, self.physics, self.av_sync)
        return sum(w * v for w, v in zip(weights, values))

    def failures(self) -> tuple[str, ...]:
        thresholds = {"identity": .95, "continuity": .90, "artifacts": .90, "physics": .85, "av_sync": .85}
        return tuple(name for name, threshold in thresholds.items() if getattr(self, name) < threshold)


def remediation(score: QAScore) -> dict:
    failures = score.failures()
    return {
        "passed": not failures,
        "overall": round(score.overall, 4),
        "failures": failures,
        "actions": tuple(f"repair_{name}" for name in failures),
    }

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class BudgetPolicy:
    max_project_credits: float = 250.0
    max_shot_credits: float = 60.0
    reserve_ratio: float = 0.15

    def usable_project_budget(self) -> float:
        return self.max_project_credits * (1.0 - self.reserve_ratio)

    def allows(self, *, project_spend: float, shot_spend: float, estimated_next: float) -> bool:
        return (
            project_spend + estimated_next <= self.usable_project_budget()
            and shot_spend + estimated_next <= self.max_shot_credits
        )

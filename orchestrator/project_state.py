from __future__ import annotations

from copy import deepcopy
from dataclasses import dataclass, field
from typing import Any


@dataclass
class ProjectState:
    project_id: str
    phase: str = "IDEA"
    version: int = 0
    canon: dict[str, Any] = field(default_factory=dict)
    production: dict[str, Any] = field(default_factory=dict)
    budgets: dict[str, Any] = field(default_factory=dict)
    approvals: dict[str, Any] = field(default_factory=dict)

    def snapshot(self) -> dict[str, Any]:
        return deepcopy({
            "project_id": self.project_id,
            "phase": self.phase,
            "version": self.version,
            "canon": self.canon,
            "production": self.production,
            "budgets": self.budgets,
            "approvals": self.approvals,
        })

    def apply_patch(self, patch: dict[str, Any]) -> None:
        for key, value in patch.items():
            if key in {"project_id", "version"}:
                continue
            current = getattr(self, key, None)
            if isinstance(current, dict) and isinstance(value, dict):
                current.update(deepcopy(value))
            elif hasattr(self, key):
                setattr(self, key, deepcopy(value))
        self.version += 1

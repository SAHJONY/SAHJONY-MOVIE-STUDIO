from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass(frozen=True)
class AgentTask:
    task_id: str
    project_id: str
    agent_role: str
    action: str
    input_state: dict[str, Any]
    constraints: dict[str, Any] = field(default_factory=dict)
    budget_credits: float | None = None
    parent_task_id: str | None = None


@dataclass(frozen=True)
class AgentDecision:
    task_id: str
    agent_role: str
    status: str
    outputs: dict[str, Any] = field(default_factory=dict)
    state_patch: dict[str, Any] = field(default_factory=dict)
    tool_requests: tuple[dict[str, Any], ...] = ()
    confidence: float = 1.0
    rationale_summary: str = ""

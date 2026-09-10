from __future__ import annotations

from dataclasses import dataclass

from .agent_contracts import AgentDecision, AgentTask
from .events import EventBus, StudioEvent
from .permissions import enforce
from .project_state import ProjectState


@dataclass
class StudioSupervisor:
    state: ProjectState
    events: EventBus

    def authorize_tool(self, role: str, tool: str) -> None:
        enforce(role, tool)

    def commit_decision(self, decision: AgentDecision) -> None:
        if decision.status not in {"completed", "approved", "rejected", "blocked"}:
            raise ValueError(f"invalid decision status: {decision.status}")
        if decision.state_patch:
            self.state.apply_patch(decision.state_patch)
        self.events.publish(StudioEvent(
            event_type="agent.decision",
            project_id=self.state.project_id,
            actor=decision.agent_role,
            payload={"task_id": decision.task_id, "status": decision.status, "outputs": decision.outputs},
        ))

    def issue_task(self, task: AgentTask) -> None:
        if task.project_id != self.state.project_id:
            raise ValueError("task project mismatch")
        self.events.publish(StudioEvent(
            event_type="agent.task.issued",
            project_id=self.state.project_id,
            actor="master_director",
            payload={"task_id": task.task_id, "role": task.agent_role, "action": task.action},
        ))

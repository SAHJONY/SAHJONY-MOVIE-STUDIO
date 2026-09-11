from __future__ import annotations

from .agent_contracts import AgentTask
from .events import StudioEvent
from .persistence import SupabaseMovieStore
from .studio_os import MovieStudioOS


PRIORITY_VALUE = {"hero": 100, "high": 75, "normal": 50, "low": 25}


class DurableMovieStudioOS(MovieStudioOS):
    """Movie OS with Supabase persistence for state, tasks, events, and provenance."""

    def __init__(self, project_id: str, store: SupabaseMovieStore) -> None:
        self.store = store
        super().__init__(project_id)

    async def bootstrap_durable(self, brief: dict) -> None:
        self.bootstrap(brief)
        await self.store.save_state(
            project_id=self.project_id,
            version=self.state.version,
            phase=self.state.phase,
            state=self.state.snapshot(),
            created_by="master_director",
        )
        await self.persist_event(self.events.events[-1])

    async def persist_event(self, event: StudioEvent) -> dict:
        return await self.store.record_event(
            project_id=event.project_id,
            event_type=event.event_type,
            source=event.actor,
            payload=event.payload,
        )

    async def enqueue_durable_task(self, task: AgentTask, *, priority: str = "normal",
                                   shot_id: str | None = None) -> dict:
        self.scheduler.submit(
            task_id=task.task_id,
            department=task.agent_role,
            payload={"action": task.action, "input_state": task.input_state},
            priority=priority,
        )
        persisted = await self.store.enqueue_task(
            project_id=task.project_id,
            agent_role=task.agent_role,
            task_type=task.action,
            task_input={
                "task_id": task.task_id,
                "input_state": task.input_state,
                "constraints": task.constraints,
                "budget_credits": task.budget_credits,
                "parent_task_id": task.parent_task_id,
            },
            priority=PRIORITY_VALUE.get(priority, 50),
            shot_id=shot_id,
        )
        await self.store.record_event(
            project_id=task.project_id,
            shot_id=shot_id,
            task_id=persisted.get("id"),
            event_type="task.queued",
            source="scheduler",
            payload={"agent_role": task.agent_role, "action": task.action, "priority": priority},
        )
        return persisted

from __future__ import annotations

from dataclasses import dataclass, field

from .cinematic_memory import CinematicMemory
from .events import EventBus, StudioEvent
from .project_state import ProjectState
from .provenance import ProvenanceLedger
from .scheduler import ProductionScheduler
from .supervisor import StudioSupervisor


@dataclass
class MovieStudioOS:
    project_id: str
    state: ProjectState = field(init=False)
    events: EventBus = field(init=False)
    memory: CinematicMemory = field(init=False)
    provenance: ProvenanceLedger = field(init=False)
    scheduler: ProductionScheduler = field(init=False)
    supervisor: StudioSupervisor = field(init=False)

    def __post_init__(self) -> None:
        self.state = ProjectState(self.project_id)
        self.events = EventBus()
        self.memory = CinematicMemory()
        self.provenance = ProvenanceLedger()
        self.scheduler = ProductionScheduler()
        self.supervisor = StudioSupervisor(self.state, self.events)

    def bootstrap(self, brief: dict) -> None:
        self.state.apply_patch({"phase": "DEVELOPMENT", "canon": {"creative_brief": brief}})
        self.events.publish(StudioEvent(
            event_type="project.bootstrapped",
            project_id=self.project_id,
            actor="master_director",
            payload={"state_version": self.state.version},
        ))

    def health(self) -> dict:
        return {
            "project_id": self.project_id,
            "phase": self.state.phase,
            "state_version": self.state.version,
            "pending_tasks": self.scheduler.pending(),
            "event_count": len(self.events.events),
            "memory_records": len(self.memory._records),
        }

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any, Callable
from uuid import uuid4


@dataclass(frozen=True)
class StudioEvent:
    event_type: str
    project_id: str
    payload: dict[str, Any]
    actor: str
    event_id: str = field(default_factory=lambda: str(uuid4()))
    created_at: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())


class EventBus:
    def __init__(self) -> None:
        self._subscribers: dict[str, list[Callable[[StudioEvent], None]]] = {}
        self.events: list[StudioEvent] = []

    def subscribe(self, event_type: str, handler: Callable[[StudioEvent], None]) -> None:
        self._subscribers.setdefault(event_type, []).append(handler)

    def publish(self, event: StudioEvent) -> None:
        self.events.append(event)
        for handler in self._subscribers.get(event.event_type, []):
            handler(event)
        for handler in self._subscribers.get("*", []):
            handler(event)

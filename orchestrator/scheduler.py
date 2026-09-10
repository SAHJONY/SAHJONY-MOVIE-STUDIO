from __future__ import annotations

from dataclasses import dataclass, field
import heapq
from typing import Any


PRIORITY = {"hero": 0, "high": 1, "normal": 2, "low": 3}


@dataclass(order=True)
class ScheduledTask:
    sort_key: tuple[int, int]
    task_id: str = field(compare=False)
    department: str = field(compare=False)
    payload: dict[str, Any] = field(compare=False, default_factory=dict)


class ProductionScheduler:
    def __init__(self) -> None:
        self._queue: list[ScheduledTask] = []
        self._counter = 0

    def submit(self, task_id: str, department: str, payload: dict[str, Any], priority: str = "normal") -> None:
        self._counter += 1
        rank = PRIORITY.get(priority, PRIORITY["normal"])
        heapq.heappush(self._queue, ScheduledTask((rank, self._counter), task_id, department, payload))

    def next(self, department: str | None = None) -> ScheduledTask | None:
        if department is None:
            return heapq.heappop(self._queue) if self._queue else None
        for idx, item in enumerate(self._queue):
            if item.department == department:
                selected = self._queue.pop(idx)
                heapq.heapify(self._queue)
                return selected
        return None

    def pending(self) -> int:
        return len(self._queue)

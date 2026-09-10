from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass
class GraphNode:
    task_id: str
    role: str
    action: str
    depends_on: set[str] = field(default_factory=set)
    payload: dict[str, Any] = field(default_factory=dict)
    status: str = "pending"


class ProductionGraph:
    def __init__(self) -> None:
        self.nodes: dict[str, GraphNode] = {}

    def add(self, node: GraphNode) -> None:
        if node.task_id in self.nodes:
            raise ValueError(f"duplicate task: {node.task_id}")
        self.nodes[node.task_id] = node

    def ready(self) -> list[GraphNode]:
        complete = {task_id for task_id, node in self.nodes.items() if node.status == "completed"}
        return [node for node in self.nodes.values() if node.status == "pending" and node.depends_on <= complete]

    def complete(self, task_id: str) -> None:
        self.nodes[task_id].status = "completed"

    def fail(self, task_id: str) -> None:
        self.nodes[task_id].status = "failed"

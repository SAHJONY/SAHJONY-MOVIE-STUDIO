from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any
from uuid import uuid4


@dataclass(frozen=True)
class ProvenanceRecord:
    artifact_id: str
    artifact_type: str
    producer: str
    inputs: tuple[str, ...] = ()
    model: str | None = None
    provider: str | None = None
    prompt_version: str | None = None
    metadata: dict[str, Any] = field(default_factory=dict)
    record_id: str = field(default_factory=lambda: str(uuid4()))
    created_at: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())


class ProvenanceLedger:
    def __init__(self) -> None:
        self.records: list[ProvenanceRecord] = []

    def append(self, record: ProvenanceRecord) -> None:
        self.records.append(record)

    def lineage(self, artifact_id: str) -> list[ProvenanceRecord]:
        direct = [r for r in self.records if r.artifact_id == artifact_id]
        input_ids = {i for r in direct for i in r.inputs}
        return direct + [r for r in self.records if r.artifact_id in input_ids]

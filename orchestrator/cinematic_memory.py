from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass
class CanonRecord:
    entity_id: str
    entity_type: str
    facts: dict[str, Any] = field(default_factory=dict)
    locked_fields: set[str] = field(default_factory=set)
    version: int = 1


class CinematicMemory:
    """Canonical structured memory. A vector store can sit beside this, never replace it."""

    def __init__(self) -> None:
        self._records: dict[str, CanonRecord] = {}

    def upsert(self, entity_id: str, entity_type: str, patch: dict[str, Any]) -> CanonRecord:
        record = self._records.get(entity_id) or CanonRecord(entity_id, entity_type)
        for key, value in patch.items():
            if key in record.locked_fields and key in record.facts and record.facts[key] != value:
                raise ValueError(f"canonical field locked: {entity_id}.{key}")
            record.facts[key] = value
        record.version += 1 if entity_id in self._records else 0
        self._records[entity_id] = record
        return record

    def lock(self, entity_id: str, *fields: str) -> None:
        self._records[entity_id].locked_fields.update(fields)

    def get(self, entity_id: str) -> CanonRecord | None:
        return self._records.get(entity_id)

    def context(self, entity_ids: list[str]) -> dict[str, dict[str, Any]]:
        return {eid: dict(self._records[eid].facts) for eid in entity_ids if eid in self._records}

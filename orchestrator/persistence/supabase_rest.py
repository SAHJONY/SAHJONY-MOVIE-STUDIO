from __future__ import annotations

import os
from typing import Any

import httpx


class SupabaseMovieStore:
    """Server-side PostgREST adapter for durable Movie OS state."""

    def __init__(self, url: str | None = None, secret: str | None = None) -> None:
        self.url = (url or os.getenv("SUPABASE_URL", "")).rstrip("/")
        self.secret = secret or os.getenv("SUPABASE_SECRET_KEY") or os.getenv("SUPABASE_SERVICE_ROLE_KEY", "")
        if not self.url or not self.secret:
            raise RuntimeError("Supabase server credentials are not configured")

    @property
    def headers(self) -> dict[str, str]:
        return {
            "apikey": self.secret,
            "Authorization": f"Bearer {self.secret}",
            "Content-Type": "application/json",
            "Prefer": "return=representation",
        }

    async def _insert(self, table: str, payload: dict[str, Any]) -> dict[str, Any]:
        async with httpx.AsyncClient(timeout=30.0) as client:
            response = await client.post(f"{self.url}/rest/v1/{table}", headers=self.headers, json=payload)
            response.raise_for_status()
            rows = response.json()
            return rows[0] if isinstance(rows, list) and rows else {}

    async def record_event(self, *, project_id: str, event_type: str, source: str,
                           payload: dict[str, Any], shot_id: str | None = None,
                           task_id: str | None = None) -> dict[str, Any]:
        body: dict[str, Any] = {
            "project_id": project_id,
            "event_type": event_type,
            "source": source,
            "payload": payload,
        }
        if shot_id:
            body["shot_id"] = shot_id
        if task_id:
            body["task_id"] = task_id
        return await self._insert("studio_events", body)

    async def enqueue_task(self, *, project_id: str, agent_role: str, task_type: str,
                           task_input: dict[str, Any], priority: int = 50,
                           shot_id: str | None = None) -> dict[str, Any]:
        body: dict[str, Any] = {
            "project_id": project_id,
            "agent_role": agent_role,
            "task_type": task_type,
            "input": task_input,
            "priority": priority,
        }
        if shot_id:
            body["shot_id"] = shot_id
        return await self._insert("agent_tasks", body)

    async def save_state(self, *, project_id: str, version: int, phase: str,
                         state: dict[str, Any], created_by: str) -> dict[str, Any]:
        return await self._insert("project_state_versions", {
            "project_id": project_id,
            "version": version,
            "phase": phase,
            "state": state,
            "created_by": created_by,
        })

    async def record_provenance(self, *, project_id: str, artifact_type: str,
                                artifact_id: str, metadata: dict[str, Any],
                                shot_id: str | None = None, provider: str | None = None,
                                model: str | None = None, prompt_hash: str | None = None) -> dict[str, Any]:
        body: dict[str, Any] = {
            "project_id": project_id,
            "artifact_type": artifact_type,
            "artifact_id": artifact_id,
            "metadata": metadata,
        }
        for key, value in {"shot_id": shot_id, "provider": provider, "model": model,
                           "prompt_hash": prompt_hash}.items():
            if value is not None:
                body[key] = value
        return await self._insert("provenance_records", body)

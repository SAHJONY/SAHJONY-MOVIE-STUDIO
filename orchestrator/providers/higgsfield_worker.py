from __future__ import annotations

import os
from dataclasses import asdict
from typing import Any

from ..models import GenerationRequest, GenerationResult
from ..persistence import SupabaseMovieStore


class HiggsfieldWorker:
    """Official SDK execution boundary with durable job provenance."""

    def __init__(self, store: SupabaseMovieStore | None = None) -> None:
        self.application = os.getenv("HF_SEEDANCE_APPLICATION", "seedance_2_5").strip() or "seedance_2_5"
        self.store = store

    @staticmethod
    def configured() -> bool:
        return bool(os.getenv("HF_KEY", "").strip()) or bool(
            os.getenv("HF_API_KEY", "").strip() and os.getenv("HF_API_SECRET", "").strip()
        )

    @staticmethod
    def _client():
        if not HiggsfieldWorker.configured():
            raise RuntimeError("Higgsfield credentials are not configured")
        import higgsfield_client
        return higgsfield_client

    async def submit(self, *, project_id: str, shot_id: str,
                     request: GenerationRequest) -> str:
        client = self._client()
        controller = await client.submit_async(
            self.application,
            arguments={
                "prompt": request.prompt,
                "mode": "t2v",
                "duration": request.duration,
                "resolution": request.params.get("resolution", "720p"),
                "generate_audio": request.params.get("generate_audio", False),
                "bitrate_mode": "high",
                "aspect_ratio": request.aspect_ratio,
            },
        )
        request_id = controller.request_id
        if self.store:
            await self.store.record_event(
                project_id=project_id,
                shot_id=shot_id,
                event_type="render.submitted",
                source="higgsfield_worker",
                payload={"request_id": request_id, "request": asdict(request)},
            )
        return request_id

    async def status(self, request_id: str) -> dict[str, Any]:
        status = await self._client().status_async(request_id=request_id)
        return {"request_id": request_id, "status": type(status).__name__.lower()}

    async def result(self, *, project_id: str, shot_id: str,
                     request_id: str, model: str) -> GenerationResult:
        raw = await self._client().result_async(request_id=request_id)
        output_uri = self._extract_output_uri(raw)
        result = GenerationResult(
            provider_job_id=request_id,
            output_uri=output_uri,
            provider="higgsfield",
            model=model,
            metadata={"raw_result": raw},
        )
        if self.store:
            await self.store.record_provenance(
                project_id=project_id,
                shot_id=shot_id,
                artifact_type="video_render",
                artifact_id=request_id,
                provider="higgsfield",
                model=model,
                metadata={"output_uri": output_uri},
            )
        return result

    async def cancel(self, request_id: str) -> None:
        await self._client().cancel_async(request_id=request_id)

    @staticmethod
    def _extract_output_uri(raw: Any) -> str:
        if isinstance(raw, str):
            return raw
        if isinstance(raw, dict):
            for key in ("url", "output_url", "video_url", "result_url"):
                value = raw.get(key)
                if isinstance(value, str) and value:
                    return value
        return ""

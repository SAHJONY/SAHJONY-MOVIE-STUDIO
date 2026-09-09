from __future__ import annotations

from typing import Any

from ..models import GenerationRequest
from ..prompt_compiler import compile_video_prompt


class HiggsfieldRouter:
    """Turns canonical shot specs into Higgsfield-compatible generation requests."""

    DRAFT_MODEL = "seedance_2_0_mini"
    FINAL_MODEL = "cinematic_studio_3_0"

    def choose_model(self, shot_spec: dict[str, Any], attempt: int) -> str:
        priority = shot_spec.get("priority", "normal")
        if priority == "hero":
            return self.FINAL_MODEL
        if attempt <= 1:
            return self.DRAFT_MODEL
        return self.FINAL_MODEL

    def build_request(self, shot_spec: dict[str, Any], attempt: int) -> GenerationRequest:
        model = self.choose_model(shot_spec, attempt)
        prompt = compile_video_prompt(shot_spec)
        refs = []
        for ref in shot_spec.get("references", []):
            if ref.get("value") and ref.get("role"):
                refs.append({"value": ref["value"], "role": ref["role"]})

        params: dict[str, Any] = {
            "resolution": "720p",
            "generate_audio": bool(shot_spec.get("audio", {}).get("generate", False)),
            "genre": shot_spec.get("style", {}).get("genre", "auto"),
        }

        return GenerationRequest(
            provider="higgsfield",
            model=model,
            prompt=prompt,
            duration=int(shot_spec.get("duration_seconds", 5)),
            aspect_ratio=shot_spec.get("aspect_ratio", "16:9"),
            params=params,
            medias=refs,
        )

    @staticmethod
    def to_tool_params(request: GenerationRequest) -> dict[str, Any]:
        payload: dict[str, Any] = {
            "model": request.model,
            "prompt": request.prompt,
            "duration": request.duration,
            "aspect_ratio": request.aspect_ratio,
            **request.params,
        }
        if request.medias:
            payload["medias"] = request.medias
        return payload

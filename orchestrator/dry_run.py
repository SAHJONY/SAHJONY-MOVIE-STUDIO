from __future__ import annotations

from typing import Any

from .provider_registry import ProviderRegistry


class DryRunPlanner:
    def __init__(self) -> None:
        self.providers = ProviderRegistry()

    def plan(self, manifest: dict[str, Any]) -> dict[str, Any]:
        rows = []
        total = 0.0
        for shot in manifest["shots"]:
            spec = {
                "shot_id": shot["shot_id"],
                "priority": shot.get("priority", "normal"),
                "duration_seconds": shot.get("duration_seconds", 5),
            }
            candidate = self.providers.candidates(spec, 1)[0]
            scale = spec["duration_seconds"] / 5.0
            estimated = round(candidate.estimated_credits_5s_720p * scale, 2)
            total += estimated
            rows.append({
                "shot_id": spec["shot_id"],
                "model": candidate.model,
                "tier": candidate.tier,
                "estimated_credits": estimated,
            })
        return {
            "project_title": manifest["project_title"],
            "duration_seconds": sum(s["duration_seconds"] for s in manifest["shots"]),
            "shot_count": len(manifest["shots"]),
            "estimated_draft_credits": round(total, 2),
            "shots": rows,
        }

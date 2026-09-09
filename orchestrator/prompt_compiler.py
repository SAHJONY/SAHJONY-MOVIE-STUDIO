from __future__ import annotations

from typing import Any


def _csv(values: dict[str, Any]) -> str:
    return ", ".join(f"{k}={v}" for k, v in values.items() if v not in (None, "", [], {}))


def compile_video_prompt(shot_spec: dict[str, Any]) -> str:
    camera = shot_spec.get("camera", {})
    lighting = shot_spec.get("lighting", {})
    style = shot_spec.get("style", {})
    performance = shot_spec.get("performance", {})
    continuity = shot_spec.get("continuity", {})

    sections = [
        shot_spec["description"].strip(),
        f"Camera: {_csv(camera)}" if camera else "",
        f"Lighting: {_csv(lighting)}" if lighting else "",
        f"Performance: {_csv(performance)}" if performance else "",
        f"Continuity constraints: {_csv(continuity)}" if continuity else "",
        f"Visual language: {_csv(style)}" if style else "",
        "Preserve character identity, wardrobe, props, screen direction, spatial geography, material texture, and shot-to-shot continuity.",
        "No unwanted text, logos, anatomy defects, temporal warping, duplicate limbs, or unexplained object changes.",
    ]
    return "\n".join(section for section in sections if section)

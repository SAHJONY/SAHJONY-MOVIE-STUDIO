from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class AgentDefinition:
    role: str
    owns: tuple[str, ...]
    can_delegate: bool = False
    approval_authority: bool = False


AGENTS = {
    "master_director": AgentDefinition("master_director", ("scope", "priority", "approvals", "budget_escalation"), True, True),
    "writer": AgentDefinition("writer", ("script", "dialogue", "story_state")),
    "continuity": AgentDefinition("continuity", ("canon", "character_state", "world_state")),
    "art_director": AgentDefinition("art_director", ("style", "assets", "visual_bible"), False, True),
    "cinematographer": AgentDefinition("cinematographer", ("camera", "lens", "blocking", "shot_geometry")),
    "lighting": AgentDefinition("lighting", ("lighting", "exposure")),
    "performance": AgentDefinition("performance", ("acting", "gesture", "facial_direction")),
    "render_worker": AgentDefinition("render_worker", ("generation", "render_job")),
    "qa": AgentDefinition("qa", ("quality_scores", "defects", "remediation")),
    "editor": AgentDefinition("editor", ("timeline", "cuts", "transitions"), False, True),
    "sound": AgentDefinition("sound", ("dialogue_audio", "sfx", "music", "mix")),
    "producer": AgentDefinition("producer", ("schedule", "resources", "costs")),
}


def get_agent(role: str) -> AgentDefinition:
    try:
        return AGENTS[role]
    except KeyError as exc:
        raise ValueError(f"unknown agent role: {role}") from exc

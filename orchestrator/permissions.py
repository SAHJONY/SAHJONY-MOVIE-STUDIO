from __future__ import annotations

ROLE_TOOLS = {
    "master_director": {"assign_task", "approve_shot", "reject_shot", "change_priority", "request_render"},
    "writer": {"write_scene", "revise_dialogue", "update_story_state"},
    "continuity": {"read_canon", "flag_continuity", "propose_state_patch"},
    "art_director": {"define_style", "approve_asset", "reject_asset"},
    "cinematographer": {"set_camera", "set_lens", "set_blocking", "set_shot_geometry"},
    "lighting": {"set_lighting", "set_exposure"},
    "render_worker": {"generate_media", "read_shot_spec"},
    "qa": {"analyze_media", "flag_issue", "recommend_rerender"},
    "editor": {"assemble_timeline", "trim_shot", "set_transition"},
}


def can_use(agent_role: str, tool_name: str) -> bool:
    return tool_name in ROLE_TOOLS.get(agent_role, set())


def enforce(agent_role: str, tool_name: str) -> None:
    if not can_use(agent_role, tool_name):
        raise PermissionError(f"{agent_role} cannot use {tool_name}")

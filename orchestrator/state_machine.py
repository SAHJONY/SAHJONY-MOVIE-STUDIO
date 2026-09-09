from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Protocol


class ShotState(str, Enum):
    PLANNED = "planned"
    READY = "ready"
    GENERATING = "generating"
    QA = "qa"
    APPROVED = "approved"
    REJECTED = "rejected"
    BLOCKED = "blocked"


@dataclass
class RenderResult:
    render_id: str
    output_uri: str
    cost_usd: float


@dataclass
class QAResult:
    passed: bool
    identity: float
    continuity: float
    artifacts: float
    av_sync: float
    physics: float
    remediation: dict


class RenderProvider(Protocol):
    def generate(self, shot_id: str, shot_spec: dict, attempt: int) -> RenderResult: ...


class QAAgent(Protocol):
    def evaluate(self, shot_id: str, render: RenderResult, acceptance: dict) -> QAResult: ...


class ShotRepository(Protocol):
    def load(self, shot_id: str) -> dict: ...
    def set_state(self, shot_id: str, state: ShotState) -> None: ...
    def record_render(self, shot_id: str, attempt: int, result: RenderResult) -> None: ...
    def record_qa(self, render_id: str, result: QAResult) -> None: ...
    def approve(self, shot_id: str, render_id: str) -> None: ...
    def patch_spec(self, shot_id: str, patch: dict) -> None: ...


def run_shot(shot_id: str, repo: ShotRepository, renderer: RenderProvider, qa: QAAgent) -> ShotState:
    shot = repo.load(shot_id)
    max_retries = int(shot.get("max_auto_retries", 2))
    shot_spec = shot["shot_spec"]
    acceptance = shot["acceptance_criteria"]
    repo.set_state(shot_id, ShotState.GENERATING)

    for attempt in range(1, max_retries + 2):
        render = renderer.generate(shot_id, shot_spec, attempt)
        repo.record_render(shot_id, attempt, render)
        repo.set_state(shot_id, ShotState.QA)
        result = qa.evaluate(shot_id, render, acceptance)
        repo.record_qa(render.render_id, result)

        if result.passed:
            repo.approve(shot_id, render.render_id)
            repo.set_state(shot_id, ShotState.APPROVED)
            return ShotState.APPROVED

        if attempt <= max_retries and result.remediation:
            repo.patch_spec(shot_id, result.remediation)
            shot_spec = {**shot_spec, **result.remediation}
            repo.set_state(shot_id, ShotState.GENERATING)
            continue

        repo.set_state(shot_id, ShotState.REJECTED)
        return ShotState.REJECTED

    repo.set_state(shot_id, ShotState.BLOCKED)
    return ShotState.BLOCKED

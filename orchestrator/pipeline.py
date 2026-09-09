from __future__ import annotations

from typing import Any, Callable

from .master_director import MasterDirector
from .providers.higgsfield import HiggsfieldRouter


GenerateFn = Callable[[dict[str, Any]], dict[str, Any]]
QaFn = Callable[[dict[str, Any], dict[str, Any]], dict[str, Any]]


class ProductionLoop:
    def __init__(self, generate: GenerateFn, evaluate: QaFn):
        self.director = MasterDirector()
        self.router = HiggsfieldRouter()
        self.generate = generate
        self.evaluate = evaluate

    def run(self, brief: dict[str, Any], shot_id: str, max_retries: int = 2) -> dict[str, Any]:
        spec = self.director.plan_shot(brief, shot_id)
        history: list[dict[str, Any]] = []

        for attempt in range(1, max_retries + 2):
            req = self.router.build_request(spec, attempt)
            tool_params = self.router.to_tool_params(req)
            generation = self.generate(tool_params)
            qa = self.evaluate(spec, generation)
            history.append({
                "attempt": attempt,
                "request": tool_params,
                "generation": generation,
                "qa": qa,
            })
            if qa.get("passed"):
                return {"status": "approved", "shot_spec": spec, "history": history}

            remediation = qa.get("remediation") or {}
            spec = {**spec, **remediation}

        return {"status": "rejected", "shot_spec": spec, "history": history}

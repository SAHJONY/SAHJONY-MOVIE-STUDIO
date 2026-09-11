import asyncio
import os
import sys
import types

from orchestrator.agent_contracts import AgentTask
from orchestrator.durable_studio import DurableMovieStudioOS
from orchestrator.models import GenerationRequest
from orchestrator.providers.higgsfield_worker import HiggsfieldWorker


class FakeStore:
    def __init__(self):
        self.states = []
        self.events = []
        self.tasks = []
        self.provenance = []

    async def save_state(self, **kwargs):
        self.states.append(kwargs); return kwargs

    async def record_event(self, **kwargs):
        self.events.append(kwargs); return {"id": "event-1", **kwargs}

    async def enqueue_task(self, **kwargs):
        self.tasks.append(kwargs); return {"id": "task-db-1", **kwargs}

    async def record_provenance(self, **kwargs):
        self.provenance.append(kwargs); return kwargs

def test_durable_bootstrap_and_task():
    async def run():
        store = FakeStore()
        studio = DurableMovieStudioOS("project-1", store)
        await studio.bootstrap_durable({"title": "Pilot"})
        task = AgentTask("task-1", "project-1", "cinematographer", "plan_shot", {"shot": 1})
        await studio.enqueue_durable_task(task, priority="hero", shot_id="shot-1")
        assert store.states[0]["phase"] == "DEVELOPMENT"
        assert store.tasks[0]["priority"] == 100
        assert studio.scheduler.pending() == 1
        assert len(store.events) == 2
    asyncio.run(run())


def test_higgsfield_worker_persists_result(monkeypatch=None):
    class Controller:
        request_id = "hf-123"

    async def submit_async(application, arguments):
        assert application == "seedance_2_5"
        assert arguments["mode"] == "t2v"
        return Controller()

    async def result_async(request_id):
        return {"video_url": "https://example.test/render.mp4"}

    fake = types.SimpleNamespace(submit_async=submit_async, result_async=result_async)
    sys.modules["higgsfield_client"] = fake
    os.environ["HF_API_KEY"] = "test-key"
    os.environ["HF_API_SECRET"] = "test-secret"

    async def run():
        store = FakeStore()
        worker = HiggsfieldWorker(store)
        request = GenerationRequest(
            provider="higgsfield",
            model="seedance_2_0_mini",
            prompt="test prompt",
            duration=5,
            aspect_ratio="16:9",
            params={"resolution": "720p"},
        )
        request_id = await worker.submit(project_id="project-1", shot_id="shot-1", request=request)
        assert request_id == "hf-123"
        result = await worker.result(
            project_id="project-1",
            shot_id="shot-1",
            request_id=request_id,
            model=request.model,
        )
        assert result.output_uri.endswith("render.mp4")
        assert store.events[0]["event_type"] == "render.submitted"
        assert store.provenance[0]["provider"] == "higgsfield"
    asyncio.run(run())

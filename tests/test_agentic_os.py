from orchestrator.agent_contracts import AgentDecision
from orchestrator.cinematic_memory import CinematicMemory
from orchestrator.cinematography import CameraCommand, resolve_handoff, check_camera_continuity
from orchestrator.events import EventBus
from orchestrator.permissions import can_use
from orchestrator.project_state import ProjectState
from orchestrator.qa_ensemble import QAScore, remediation
from orchestrator.scheduler import ProductionScheduler
from orchestrator.studio_os import MovieStudioOS
from orchestrator.supervisor import StudioSupervisor


def test_camera_handoff_and_continuity():
    active = CameraCommand(verb="orbit", subject="ARIA", duration_s=5)
    incoming = CameraCommand(verb="orbit", subject="ARIA", duration_s=5)
    assert resolve_handoff(active, incoming).action == "blend"
    check = check_camera_continuity({"screen_direction": "L2R", "eyeline_axis": "A"}, incoming)
    assert check.ok


def test_locked_canon_rejects_drift():
    memory = CinematicMemory()
    memory.upsert("ARIA", "character", {"coat": "red", "eyes": "green"})
    memory.lock("ARIA", "eyes")
    try:
        memory.upsert("ARIA", "character", {"eyes": "blue"})
    except ValueError:
        pass
    else:
        raise AssertionError("locked canon accepted drift")


def test_permissions_and_supervisor():
    assert can_use("cinematographer", "set_camera")
    assert not can_use("writer", "generate_media")
    state = ProjectState("p1")
    bus = EventBus()
    supervisor = StudioSupervisor(state, bus)
    supervisor.commit_decision(AgentDecision(
        task_id="t1", agent_role="writer", status="completed",
        state_patch={"canon": {"scene_1": "locked"}},
    ))
    assert state.version == 1
    assert len(bus.events) == 1


def test_scheduler_prioritizes_hero():
    scheduler = ProductionScheduler()
    scheduler.submit("normal", "render", {}, "normal")
    scheduler.submit("hero", "render", {}, "hero")
    assert scheduler.next().task_id == "hero"


def test_qa_ensemble_requires_identity():
    result = remediation(QAScore(.90, .99, .99, .99, .99))
    assert not result["passed"]
    assert "identity" in result["failures"]


def test_movie_studio_bootstrap():
    studio = MovieStudioOS("movie-001")
    studio.bootstrap({"title": "Test Film"})
    health = studio.health()
    assert health["phase"] == "DEVELOPMENT"
    assert health["state_version"] == 1


def test_production_graph_dependencies():
    from orchestrator.task_graph import GraphNode, ProductionGraph
    graph = ProductionGraph()
    graph.add(GraphNode("script", "writer", "write_scene"))
    graph.add(GraphNode("board", "art_director", "storyboard", {"script"}))
    assert [n.task_id for n in graph.ready()] == ["script"]
    graph.complete("script")
    assert [n.task_id for n in graph.ready()] == ["board"]


def test_approval_gate():
    from orchestrator.approval_gates import evaluate_gate
    assert evaluate_gate("shot_lock", {"identity": .97, "continuity": .94, "artifacts": .95})
    assert not evaluate_gate("shot_lock", {"identity": .90, "continuity": .94, "artifacts": .95})


def test_provider_circuit_breaker():
    from orchestrator.provider_governor import ProviderGovernor
    governor = ProviderGovernor(failure_threshold=2, cooldown_seconds=60)
    governor.record_failure("x")
    assert governor.available("x")
    governor.record_failure("x")
    assert not governor.available("x")


def test_capability_registry_prefers_quality():
    from orchestrator.model_capabilities import CapabilityRegistry, ModelCapability
    registry = CapabilityRegistry()
    registry.register(ModelCapability("p1", "draft", frozenset({"video"}), frozenset({"references"}), quality_rank=2, cost_rank=1))
    registry.register(ModelCapability("p2", "hero", frozenset({"video"}), frozenset({"references"}), quality_rank=5, cost_rank=3))
    matches = registry.match(modality="video", needs={"references"})
    assert matches[0].model == "hero"

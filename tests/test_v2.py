import json
from pathlib import Path

from orchestrator.budget import BudgetPolicy
from orchestrator.dry_run import DryRunPlanner
from orchestrator.provider_registry import ProviderRegistry


def load_manifest():
    path = Path(__file__).parents[1] / "examples" / "first_autonomous_sequence.json"
    return json.loads(path.read_text())


def test_first_sequence_is_45_seconds():
    manifest = load_manifest()
    assert len(manifest["shots"]) == 9
    assert sum(s["duration_seconds"] for s in manifest["shots"]) == 45


def test_hero_routes_premium():
    hero = {"priority": "hero", "duration_seconds": 5}
    assert ProviderRegistry().candidates(hero, 1)[0].model == "cinematic_studio_3_0"


def test_normal_routes_draft():
    normal = {"priority": "normal", "duration_seconds": 5}
    assert ProviderRegistry().candidates(normal, 1)[0].model == "seedance_2_0_mini"


def test_budget_guard():
    policy = BudgetPolicy(max_project_credits=100, max_shot_credits=30, reserve_ratio=.1)
    assert policy.allows(project_spend=20, shot_spend=0, estimated_next=12.5)
    assert not policy.allows(project_spend=89, shot_spend=0, estimated_next=12.5)
    assert not policy.allows(project_spend=0, shot_spend=25, estimated_next=12.5)


def test_dry_run_costs():
    plan = DryRunPlanner().plan(load_manifest())
    assert plan["duration_seconds"] == 45
    assert plan["shot_count"] == 9
    assert plan["estimated_draft_credits"] == 162.5

from orchestrator.master_director import MasterDirector
from orchestrator.providers.higgsfield import HiggsfieldRouter
from orchestrator.qa_policy import AcceptancePolicy


def sample_brief():
    return {
        "description": "A puppet-like explorer crosses a miniature bridge in rain.",
        "duration_seconds": 5,
        "style": {"genre": "drama"},
        "continuity": {"coat": "yellow"},
    }


def test_director_emits_canonical_spec():
    spec = MasterDirector().plan_shot(sample_brief(), "S1")
    assert spec["shot_id"] == "S1"
    assert spec["duration_seconds"] == 5
    assert spec["camera"]["lens_mm"] == 50


def test_router_uses_draft_then_final():
    spec = MasterDirector().plan_shot(sample_brief(), "S1")
    router = HiggsfieldRouter()
    assert router.build_request(spec, 1).model == "seedance_2_0_mini"
    assert router.build_request(spec, 2).model == "cinematic_studio_3_0"


def test_hero_uses_final_immediately():
    brief = sample_brief() | {"priority": "hero"}
    spec = MasterDirector().plan_shot(brief, "S1")
    assert HiggsfieldRouter().build_request(spec, 1).model == "cinematic_studio_3_0"


def test_qa_policy():
    policy = AcceptancePolicy()
    good = {"identity": .97, "continuity": .93, "artifacts": .95, "physics": .9, "av_sync": .9}
    bad = good | {"identity": .7}
    assert policy.passes(good)
    assert not policy.passes(bad)
    assert policy.remediation(bad)["qa_remediation"]

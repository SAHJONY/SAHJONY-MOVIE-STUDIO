from orchestrator.continuity_gate import ContinuityGate
from orchestrator.identity_engine import IdentityPack


def pack():
    return IdentityPack(
        character_id="char-1",
        canonical_id="TRAVELER_001",
        wardrobe_profile={"coat": "mustard raincoat", "boots": "dark boots", "scarf": "red scarf"},
    )


def test_continuity_gate_passes_locked_state():
    shot = {"continuity": {
        "character_id": "TRAVELER_001",
        "wardrobe": "mustard raincoat, dark boots, red scarf",
        "hero_prop": "weathered brass compass",
        "weather": "continuous rain",
    }}
    result = ContinuityGate().evaluate(shot, pack(), {
        "hero_prop": "weathered brass compass",
        "weather": "continuous rain",
    })
    assert result.passed


def test_continuity_gate_returns_minimal_patch():
    shot = {"continuity": {
        "character_id": "TRAVELER_001",
        "wardrobe": "mustard raincoat, dark boots, red scarf",
        "hero_prop": "glass compass",
        "weather": "dry",
    }}
    result = ContinuityGate().evaluate(shot, pack(), {
        "hero_prop": "weathered brass compass",
        "weather": "continuous rain",
    })
    assert not result.passed
    assert result.required_patch["continuity"]["weather"] == "continuous rain"

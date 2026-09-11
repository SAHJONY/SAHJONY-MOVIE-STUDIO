from orchestrator.identity_engine import CharacterIdentityEngine, IdentityPack


def traveler_pack():
    return IdentityPack(
        character_id="char-1",
        canonical_id="TRAVELER_001",
        immutable_traits={"silhouette": "locked"},
        wardrobe_profile={"coat": "mustard raincoat", "boots": "dark boots", "scarf": "red scarf"},
        negative_constraints=("no wardrobe color drift", "no proportion drift"),
        identity_threshold=0.95,
    )


def test_identity_engine_accepts_canonical_shot():
    engine = CharacterIdentityEngine()
    shot = {"continuity": {"character_id": "TRAVELER_001", "wardrobe": "mustard raincoat, dark boots, red scarf"}}
    result = engine.validate_shot_spec(shot, traveler_pack())
    assert result.passed
    assert result.score == 1.0


def test_identity_engine_blocks_wardrobe_drift():
    engine = CharacterIdentityEngine()
    shot = {"continuity": {"character_id": "TRAVELER_001", "wardrobe": "blue coat, dark boots"}}
    result = engine.validate_shot_spec(shot, traveler_pack())
    assert not result.passed
    assert "wardrobe drift" in result.violations


def test_identity_render_gate_requires_threshold():
    engine = CharacterIdentityEngine()
    pack = traveler_pack()
    assert engine.evaluate_render(0.96, [], pack).passed
    assert not engine.evaluate_render(0.94, [], pack).passed

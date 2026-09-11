from orchestrator.provider_governor import ProviderGovernor


def test_fatal_provider_failure_blocks_immediately():
    governor = ProviderGovernor(failure_threshold=3)
    governor.record_failure("higgsfield", reason="auth_invalid")
    assert not governor.available("higgsfield")
    assert governor.health["higgsfield"].blocked is True
    assert governor.health["higgsfield"].block_reason == "auth_invalid"


def test_transient_failure_uses_threshold():
    governor = ProviderGovernor(failure_threshold=2, cooldown_seconds=60)
    governor.record_failure("renderer", reason="transient")
    assert governor.available("renderer")
    governor.record_failure("renderer", reason="transient")
    assert not governor.available("renderer")


def test_success_unblocks_provider():
    governor = ProviderGovernor()
    governor.record_failure("higgsfield", reason="plan_ineligible")
    assert not governor.available("higgsfield")
    governor.record_success("higgsfield", latency_ms=100)
    assert governor.available("higgsfield")
    assert governor.health["higgsfield"].block_reason is None

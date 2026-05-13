from __future__ import annotations

from MAKSIMAR_SERVER.CLIENT_LEARNING_INPUT import build_client_metrics_filter_policy


def test_client_metrics_filter_models_smoke() -> None:
    policy = build_client_metrics_filter_policy()

    assert policy.filter_policy_ready is True
    assert len(policy.signals) >= 5
    assert policy.source_bound_required is True
    assert policy.tenant_boundary_required is True
    assert policy.personal_data_redaction_required is True
    assert policy.raw_payload_allowed is False
    assert policy.automatic_training_allowed is False

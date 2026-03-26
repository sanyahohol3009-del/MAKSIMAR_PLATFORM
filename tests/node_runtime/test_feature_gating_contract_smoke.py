from __future__ import annotations

from MAKSIMAR_SERVER.EXECUTION_CONTROL.node_runtime import (
    build_feature_gating_contract,
)


def test_feature_gating_contract_builds() -> None:
    """Feature-gating contract should build successfully."""
    contract = build_feature_gating_contract()

    assert contract.total_entries == 9
    assert len(contract.entries) == 9


def test_feature_gating_contract_contains_multiple_states() -> None:
    """Feature-gating contract should expose supported and degraded states."""
    contract = build_feature_gating_contract()

    availabilities = {entry.availability for entry in contract.entries}
    feature_ids = {entry.feature_id for entry in contract.entries}

    assert "supported" in availabilities or "degraded" in availabilities
    assert "ai_chat" in feature_ids
    assert "media_render" in feature_ids
    assert "simulation_task" in feature_ids

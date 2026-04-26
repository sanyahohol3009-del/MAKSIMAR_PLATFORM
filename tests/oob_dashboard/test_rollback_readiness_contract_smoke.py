from __future__ import annotations

from MAKSIMAR_CORE_LIB.oob_dashboard.rollback_readiness_contract import (
    build_rollback_readiness_contract,
)


def test_rollback_readiness_contract_builds() -> None:
    """Rollback readiness contract should build successfully."""
    contract = build_rollback_readiness_contract()

    assert contract.contract_id == "rollback_readiness_contract_001"
    assert contract.total_entries == 3
    assert contract.read_only_rollback_entries == 2
    assert contract.approval_bound_rollback_entries == 1
    assert contract.rollback_visible_entries == 3
    assert contract.operator_visible_entries == 3


def test_rollback_readiness_contract_contains_expected_entries() -> None:
    """Rollback readiness contract should contain expected canonical entries."""
    contract = build_rollback_readiness_contract()
    entry_map = {entry.operator_intent_id: entry for entry in contract.entries}

    assert (
        entry_map["operator_intent_001"].rollback_readiness_class
        == "read_only_rollback_readiness"
    )
    assert (
        entry_map["operator_intent_001"].rollback_readiness_mode
        == "preview_review_simulation_replay_sandbox_risk_rollback_readiness"
    )
    assert entry_map["operator_intent_001"].panel_id == "action_queue"

    assert (
        entry_map["operator_intent_002"].rollback_readiness_class
        == "read_only_rollback_readiness"
    )
    assert entry_map["operator_intent_002"].panel_id == "action_queue"

    assert (
        entry_map["operator_intent_003"].rollback_readiness_class
        == "approval_bound_rollback_readiness"
    )
    assert (
        entry_map["operator_intent_003"].rollback_readiness_mode
        == "preview_review_approval_simulation_replay_sandbox_risk_rollback_readiness"
    )
    assert entry_map["operator_intent_003"].panel_id == "approval_queue"

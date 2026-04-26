from __future__ import annotations

from MAKSIMAR_CORE_LIB.oob_dashboard.risk_summary_contract import (
    build_risk_summary_contract,
)


def test_risk_summary_contract_builds() -> None:
    """Risk summary contract should build successfully."""
    contract = build_risk_summary_contract()

    assert contract.contract_id == "risk_summary_contract_001"
    assert contract.total_entries == 3
    assert contract.read_only_risk_entries == 2
    assert contract.approval_bound_risk_entries == 1
    assert contract.risk_visible_entries == 3
    assert contract.operator_visible_entries == 3


def test_risk_summary_contract_contains_expected_entries() -> None:
    """Risk summary contract should contain expected canonical entries."""
    contract = build_risk_summary_contract()
    entry_map = {entry.operator_intent_id: entry for entry in contract.entries}

    assert (
        entry_map["operator_intent_001"].risk_summary_class
        == "read_only_risk_summary"
    )
    assert (
        entry_map["operator_intent_001"].risk_summary_mode
        == "preview_review_simulation_replay_sandbox_risk_summary"
    )
    assert entry_map["operator_intent_001"].panel_id == "action_queue"

    assert (
        entry_map["operator_intent_002"].risk_summary_class
        == "read_only_risk_summary"
    )
    assert entry_map["operator_intent_002"].panel_id == "action_queue"

    assert (
        entry_map["operator_intent_003"].risk_summary_class
        == "approval_bound_risk_summary"
    )
    assert (
        entry_map["operator_intent_003"].risk_summary_mode
        == "preview_review_approval_simulation_replay_sandbox_risk_summary"
    )
    assert entry_map["operator_intent_003"].panel_id == "approval_queue"

from __future__ import annotations

from MAKSIMAR_CORE_LIB.oob_dashboard.simulation_result_contract import (
    build_simulation_result_contract,
)


def test_simulation_result_contract_builds() -> None:
    """Simulation result contract should build successfully."""
    contract = build_simulation_result_contract()

    assert contract.contract_id == "simulation_result_contract_001"
    assert contract.total_entries == 3
    assert contract.read_only_simulation_entries == 2
    assert contract.approval_bound_simulation_entries == 1
    assert contract.review_visible_entries == 3
    assert contract.operator_visible_entries == 3


def test_simulation_result_contract_contains_expected_entries() -> None:
    """Simulation result contract should contain expected canonical entries."""
    contract = build_simulation_result_contract()
    entry_map = {entry.operator_intent_id: entry for entry in contract.entries}

    assert (
        entry_map["operator_intent_001"].simulation_result_class
        == "read_only_simulation_result"
    )
    assert (
        entry_map["operator_intent_001"].simulation_evidence_mode
        == "preview_review_simulation_evidence"
    )
    assert entry_map["operator_intent_001"].panel_id == "action_queue"

    assert (
        entry_map["operator_intent_002"].simulation_result_class
        == "read_only_simulation_result"
    )
    assert entry_map["operator_intent_002"].panel_id == "action_queue"

    assert (
        entry_map["operator_intent_003"].simulation_result_class
        == "approval_bound_simulation_result"
    )
    assert (
        entry_map["operator_intent_003"].simulation_evidence_mode
        == "preview_review_approval_simulation_evidence"
    )
    assert entry_map["operator_intent_003"].panel_id == "approval_queue"

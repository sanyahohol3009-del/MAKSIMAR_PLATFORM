from __future__ import annotations

from MAKSIMAR_CORE_LIB.oob_dashboard.sandbox_route_contract import (
    build_sandbox_route_contract,
)


def test_sandbox_route_contract_builds() -> None:
    """Sandbox route contract should build successfully."""
    contract = build_sandbox_route_contract()

    assert contract.contract_id == "sandbox_route_contract_001"
    assert contract.total_entries == 3
    assert contract.read_only_sandbox_entries == 2
    assert contract.approval_bound_sandbox_entries == 1
    assert contract.sandbox_visible_entries == 3
    assert contract.operator_visible_entries == 3


def test_sandbox_route_contract_contains_expected_entries() -> None:
    """Sandbox route contract should contain expected canonical entries."""
    contract = build_sandbox_route_contract()
    entry_map = {entry.operator_intent_id: entry for entry in contract.entries}

    assert (
        entry_map["operator_intent_001"].sandbox_route_class
        == "read_only_sandbox_route"
    )
    assert (
        entry_map["operator_intent_001"].sandbox_route_mode
        == "preview_review_simulation_replay_sandbox_route"
    )
    assert entry_map["operator_intent_001"].panel_id == "action_queue"

    assert (
        entry_map["operator_intent_002"].sandbox_route_class
        == "read_only_sandbox_route"
    )
    assert entry_map["operator_intent_002"].panel_id == "action_queue"

    assert (
        entry_map["operator_intent_003"].sandbox_route_class
        == "approval_bound_sandbox_route"
    )
    assert (
        entry_map["operator_intent_003"].sandbox_route_mode
        == "preview_review_approval_simulation_replay_sandbox_route"
    )
    assert entry_map["operator_intent_003"].panel_id == "approval_queue"

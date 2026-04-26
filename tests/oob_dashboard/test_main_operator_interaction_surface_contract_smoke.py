from __future__ import annotations

from MAKSIMAR_CORE_LIB.oob_dashboard.main_operator_interaction_surface_contract import (
    build_main_operator_interaction_surface_contract,
)


def test_main_operator_interaction_surface_contract_builds() -> None:
    """Main operator interaction surface contract should build successfully."""
    contract = build_main_operator_interaction_surface_contract()

    assert contract.contract_id == "main_operator_interaction_surface_contract_001"
    assert contract.total_entries == 3
    assert contract.read_only_surface_entries == 2
    assert contract.approval_bound_surface_entries == 1
    assert contract.pending_approval_visible_entries == 1
    assert contract.handoff_ready_entries == 3
    assert contract.audit_visible_entries == 3
    assert contract.operator_visible_entries == 3


def test_main_operator_interaction_surface_contract_contains_expected_surface_classes() -> None:
    """Surface contract should preserve read-only and approval-bound interaction semantics."""
    contract = build_main_operator_interaction_surface_contract()
    entry_map = {entry.operator_intent_id: entry for entry in contract.entries}

    assert entry_map["operator_intent_001"].surface_class == "read_only_surface"
    assert entry_map["operator_intent_001"].intent_kind == "view_request"
    assert entry_map["operator_intent_001"].pending_approval_visible is False

    assert entry_map["operator_intent_002"].surface_class == "read_only_surface"
    assert entry_map["operator_intent_002"].intent_kind == "navigation_request"
    assert entry_map["operator_intent_002"].pending_approval_visible is False

    assert entry_map["operator_intent_003"].surface_class == "approval_bound_surface"
    assert entry_map["operator_intent_003"].intent_kind == "control_request"
    assert entry_map["operator_intent_003"].pending_approval_visible is True

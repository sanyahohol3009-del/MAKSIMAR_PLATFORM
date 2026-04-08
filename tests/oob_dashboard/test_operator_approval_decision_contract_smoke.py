from __future__ import annotations

from MAKSIMAR_CORE_LIB.oob_dashboard.operator_approval_decision_contract import (
    build_operator_approval_decision_contract,
)


def test_operator_approval_decision_contract_builds() -> None:
    """Operator approval decision contract should build successfully."""
    contract = build_operator_approval_decision_contract()

    assert contract.contract_id == "operator_approval_decision_contract_001"
    assert contract.total_entries == 3
    assert contract.structurally_valid_entries == 3
    assert contract.allowed_entries == 2
    assert contract.blocked_entries == 0
    assert contract.pending_approval_entries == 1
    assert contract.deferred_entries == 0
    assert contract.executable_after_approval_entries == 1
    assert contract.operator_visible_entries == 3


def test_operator_approval_decision_contract_marks_registered_structures() -> None:
    """Operator approval decision contract should mark all canonical structures as registered."""
    contract = build_operator_approval_decision_contract()

    for entry in contract.entries:
        assert entry.intent_registered is True
        assert entry.policy_status_registered is True
        assert entry.approval_requirement_registered is True
        assert entry.reason_code_registered is True
        assert entry.structurally_valid is True


def test_operator_approval_decision_contract_contains_expected_allowed_entries() -> None:
    """Operator approval decision contract should contain expected allowed entries."""
    contract = build_operator_approval_decision_contract()
    entry_map = {entry.operator_intent_id: entry for entry in contract.entries}

    view_entry = entry_map["operator_intent_001"]
    navigation_entry = entry_map["operator_intent_002"]

    assert view_entry.policy_decision_status == "allowed"
    assert view_entry.approval_requirement == "no_approval_required"
    assert view_entry.reason_code == "operator_surface_allowed"
    assert view_entry.executable_after_approval is False
    assert view_entry.explanation_visible_to_operator is True

    assert navigation_entry.policy_decision_status == "allowed"
    assert navigation_entry.approval_requirement == "no_approval_required"
    assert navigation_entry.reason_code == "operator_surface_allowed"


def test_operator_approval_decision_contract_contains_expected_pending_entry() -> None:
    """Operator approval decision contract should contain expected pending approval entry."""
    contract = build_operator_approval_decision_contract()
    entry_map = {entry.operator_intent_id: entry for entry in contract.entries}

    control_entry = entry_map["operator_intent_003"]

    assert control_entry.policy_decision_status == "pending_approval"
    assert control_entry.approval_requirement == "human_approval_required"
    assert control_entry.reason_code == "approval_required"
    assert control_entry.executable_after_approval is True
    assert control_entry.explanation_visible_to_operator is True


def test_operator_approval_decision_contract_preserves_trace_visibility() -> None:
    """Operator approval decision contract should preserve canonical trace visibility."""
    contract = build_operator_approval_decision_contract()

    for entry in contract.entries:
        assert entry.trace_id.startswith("trace_operator_intent_")


def test_operator_approval_decision_contract_has_no_blocked_or_deferred_entries_in_baseline() -> None:
    """Baseline operator approval decision contract should not yet contain blocked or deferred entries."""
    contract = build_operator_approval_decision_contract()

    blocked_entries = [
        entry for entry in contract.entries if entry.policy_decision_status == "blocked"
    ]
    deferred_entries = [
        entry for entry in contract.entries if entry.policy_decision_status == "deferred"
    ]

    assert blocked_entries == []
    assert deferred_entries == []

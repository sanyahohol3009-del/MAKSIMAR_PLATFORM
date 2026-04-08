from __future__ import annotations

from MAKSIMAR_CORE_LIB.oob_dashboard.operator_intent_models import (
    ALL_INTENT_KINDS,
    ALL_INTENT_STATES,
    ALL_REQUESTED_ACTION_KINDS,
)
from MAKSIMAR_CORE_LIB.oob_dashboard.operator_intent_vocabulary_contract import (
    build_operator_intent_vocabulary_contract,
)


def test_operator_intent_vocabulary_contract_builds() -> None:
    """Operator intent vocabulary contract should build successfully."""
    contract = build_operator_intent_vocabulary_contract()

    assert contract.contract_id == "operator_intent_vocabulary_contract_001"
    assert contract.total_entries == (
        len(ALL_INTENT_KINDS)
        + len(ALL_INTENT_STATES)
        + len(ALL_REQUESTED_ACTION_KINDS)
    )
    assert contract.intent_kind_entries == len(ALL_INTENT_KINDS)
    assert contract.intent_state_entries == len(ALL_INTENT_STATES)
    assert contract.requested_action_entries == len(ALL_REQUESTED_ACTION_KINDS)


def test_operator_intent_vocabulary_contract_is_operator_readable() -> None:
    """All operator intent vocabulary entries should remain operator readable."""
    contract = build_operator_intent_vocabulary_contract()

    assert contract.operator_readable_entries == contract.total_entries
    assert all(entry.operator_readable for entry in contract.entries)


def test_operator_intent_vocabulary_contract_contains_expected_groups() -> None:
    """Operator intent vocabulary contract should contain expected vocabulary groups."""
    contract = build_operator_intent_vocabulary_contract()

    groups = {entry.vocabulary_group for entry in contract.entries}

    assert groups == {"intent_kind", "intent_state", "requested_action"}


def test_operator_intent_vocabulary_contract_contains_expected_intent_kind_values() -> None:
    """Operator intent vocabulary contract should include canonical intent kinds."""
    contract = build_operator_intent_vocabulary_contract()

    kind_values = {
        entry.canonical_value
        for entry in contract.entries
        if entry.vocabulary_group == "intent_kind"
    }

    assert kind_values == set(ALL_INTENT_KINDS)


def test_operator_intent_vocabulary_contract_contains_expected_intent_state_values() -> None:
    """Operator intent vocabulary contract should include canonical intent states."""
    contract = build_operator_intent_vocabulary_contract()

    state_values = {
        entry.canonical_value
        for entry in contract.entries
        if entry.vocabulary_group == "intent_state"
    }

    assert state_values == set(ALL_INTENT_STATES)


def test_operator_intent_vocabulary_contract_contains_expected_requested_action_values() -> None:
    """Operator intent vocabulary contract should include canonical requested actions."""
    contract = build_operator_intent_vocabulary_contract()

    action_values = {
        entry.canonical_value
        for entry in contract.entries
        if entry.vocabulary_group == "requested_action"
    }

    assert action_values == set(ALL_REQUESTED_ACTION_KINDS)


def test_operator_intent_vocabulary_contract_marks_approval_relevant_values() -> None:
    """Operator intent vocabulary contract should mark approval-relevant values."""
    contract = build_operator_intent_vocabulary_contract()

    approval_relevant_values = {
        entry.canonical_value
        for entry in contract.entries
        if entry.approval_relevant
    }

    assert "control_request" in approval_relevant_values
    assert "approval_request" in approval_relevant_values
    assert "system_action_request" in approval_relevant_values
    assert "intent_pending_approval" in approval_relevant_values
    assert "intent_approved" in approval_relevant_values
    assert "intent_rejected" in approval_relevant_values
    assert "request_control_surface" in approval_relevant_values
    assert "request_approval_flow" in approval_relevant_values
    assert "request_system_action" in approval_relevant_values


def test_operator_intent_vocabulary_contract_marks_handoff_relevant_values() -> None:
    """Operator intent vocabulary contract should mark handoff-relevant values."""
    contract = build_operator_intent_vocabulary_contract()

    handoff_relevant_values = {
        entry.canonical_value
        for entry in contract.entries
        if entry.handoff_relevant
    }

    assert "control_request" in handoff_relevant_values
    assert "system_action_request" in handoff_relevant_values
    assert "intent_handoff_ready" in handoff_relevant_values
    assert "intent_handed_off" in handoff_relevant_values
    assert "request_control_surface" in handoff_relevant_values
    assert "request_system_action" in handoff_relevant_values


def test_operator_intent_vocabulary_contract_exposes_stable_display_labels() -> None:
    """Operator intent vocabulary contract should expose stable display labels."""
    contract = build_operator_intent_vocabulary_contract()

    entry_map = {entry.canonical_value: entry for entry in contract.entries}

    assert entry_map["view_request"].display_label == "View Request"
    assert entry_map["intent_pending_approval"].display_label == "Intent Pending Approval"
    assert entry_map["request_system_action"].display_label == "Request System Action"

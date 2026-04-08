from __future__ import annotations

import pytest

from MAKSIMAR_CORE_LIB.oob_dashboard.operator_audit_visibility_contract import (
    OperatorAuditVisibilityContractEntry,
    build_operator_audit_visibility_contract,
)


def test_operator_audit_visibility_contract_builds() -> None:
    """Operator audit visibility contract should build successfully."""
    contract = build_operator_audit_visibility_contract()

    assert contract.contract_id == "operator_audit_visibility_contract_001"
    assert contract.total_entries == 3
    assert contract.read_only_entries == 2
    assert contract.approval_bound_entries == 1
    assert contract.blocked_entries == 0
    assert contract.failure_entries == 0
    assert contract.operator_visible_entries == 3
    assert contract.trace_required_entries == 3
    assert contract.structurally_valid_entries == 3


def test_operator_audit_visibility_contract_contains_expected_entries() -> None:
    """Operator audit visibility contract should contain expected canonical entries."""
    contract = build_operator_audit_visibility_contract()
    entry_map = {entry.operator_intent_id: entry for entry in contract.entries}

    assert entry_map["operator_intent_001"].audit_visibility_state == "audit_visible_read_only"
    assert entry_map["operator_intent_001"].audit_event_class == "read_only_navigation"

    assert entry_map["operator_intent_002"].audit_visibility_state == "audit_visible_read_only"
    assert entry_map["operator_intent_002"].audit_event_class == "read_only_navigation"

    assert entry_map["operator_intent_003"].audit_visibility_state == "audit_visible_approval_bound"
    assert entry_map["operator_intent_003"].audit_event_class == "approval_bound_control"


def test_operator_audit_visibility_contract_preserves_registration_flags() -> None:
    """Operator audit visibility contract should preserve canonical registration flags."""
    contract = build_operator_audit_visibility_contract()

    for entry in contract.entries:
        assert entry.state_registered is True
        assert entry.event_class_registered is True
        assert entry.structurally_valid is True
        assert entry.operator_visible is True
        assert entry.requires_audit_trace is True


def test_operator_audit_visibility_contract_entry_rejects_blank_id() -> None:
    """Operator audit visibility contract entry should reject blank ids."""
    with pytest.raises(ValueError, match="audit_event_id must be a non-empty string."):
        OperatorAuditVisibilityContractEntry(
            audit_event_id="",
            handoff_id="operator_handoff_001",
            operator_intent_id="operator_intent_001",
            audit_visibility_state="audit_visible_read_only",
            audit_event_class="read_only_navigation",
            operator_visible=True,
            requires_audit_trace=True,
            state_registered=True,
            event_class_registered=True,
            structurally_valid=True,
            trace_id="trace_operator_intent_invalid",
            description="Invalid audit contract entry.",
        )


def test_operator_audit_visibility_contract_entry_rejects_invalid_state_registration() -> None:
    """Operator audit visibility contract entry should reject false state registration."""
    with pytest.raises(ValueError, match="state_registered must be true"):
        OperatorAuditVisibilityContractEntry(
            audit_event_id="audit_visibility_invalid_registration",
            handoff_id="operator_handoff_001",
            operator_intent_id="operator_intent_001",
            audit_visibility_state="audit_visible_read_only",
            audit_event_class="read_only_navigation",
            operator_visible=True,
            requires_audit_trace=True,
            state_registered=False,
            event_class_registered=True,
            structurally_valid=True,
            trace_id="trace_operator_intent_invalid_registration",
            description="Invalid audit contract registration.",
        )


def test_operator_audit_visibility_contract_entry_rejects_invalid_event_registration() -> None:
    """Operator audit visibility contract entry should reject false event-class registration."""
    with pytest.raises(ValueError, match="event_class_registered must be true"):
        OperatorAuditVisibilityContractEntry(
            audit_event_id="audit_visibility_invalid_event_registration",
            handoff_id="operator_handoff_001",
            operator_intent_id="operator_intent_001",
            audit_visibility_state="audit_visible_read_only",
            audit_event_class="read_only_navigation",
            operator_visible=True,
            requires_audit_trace=True,
            state_registered=True,
            event_class_registered=False,
            structurally_valid=True,
            trace_id="trace_operator_intent_invalid_event_registration",
            description="Invalid audit contract event registration.",
        )

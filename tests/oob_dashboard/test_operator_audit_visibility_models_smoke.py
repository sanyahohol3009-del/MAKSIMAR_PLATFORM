from __future__ import annotations

import pytest

from MAKSIMAR_CORE_LIB.oob_dashboard.operator_audit_visibility_models import (
    ALL_AUDIT_EVENT_CLASSES,
    ALL_AUDIT_VISIBILITY_STATES,
    OperatorAuditVisibilityEntry,
    build_operator_audit_visibility_model,
)


def test_operator_audit_visibility_model_builds() -> None:
    """Operator audit visibility model should build successfully."""
    model = build_operator_audit_visibility_model()

    assert model.model_id == "operator_audit_visibility_model_001"
    assert model.total_entries == 3
    assert model.read_only_entries == 2
    assert model.approval_bound_entries == 1
    assert model.blocked_entries == 0
    assert model.failure_entries == 0
    assert model.operator_visible_entries == 3
    assert model.trace_required_entries == 3


def test_operator_audit_visibility_model_contains_expected_entries() -> None:
    """Operator audit visibility model should contain expected canonical entries."""
    model = build_operator_audit_visibility_model()
    entry_map = {entry.operator_intent_id: entry for entry in model.entries}

    assert entry_map["operator_intent_001"].audit_visibility_state == "audit_visible_read_only"
    assert entry_map["operator_intent_001"].audit_event_class == "read_only_navigation"

    assert entry_map["operator_intent_002"].audit_visibility_state == "audit_visible_read_only"
    assert entry_map["operator_intent_002"].audit_event_class == "read_only_navigation"

    assert entry_map["operator_intent_003"].audit_visibility_state == "audit_visible_approval_bound"
    assert entry_map["operator_intent_003"].audit_event_class == "approval_bound_control"


def test_operator_audit_visibility_model_preserves_trace_visibility() -> None:
    """Operator audit visibility model should preserve trace visibility."""
    model = build_operator_audit_visibility_model()

    for entry in model.entries:
        assert entry.operator_visible is True
        assert entry.requires_audit_trace is True
        assert entry.trace_id.startswith("trace_operator_intent_")


def test_operator_audit_visibility_entry_rejects_blank_id() -> None:
    """Operator audit visibility entry should reject blank audit ids."""
    with pytest.raises(ValueError, match="audit_event_id must be a non-empty string."):
        OperatorAuditVisibilityEntry(
            audit_event_id="",
            handoff_id="operator_handoff_001",
            operator_intent_id="operator_intent_001",
            audit_visibility_state="audit_visible_read_only",
            audit_event_class="read_only_navigation",
            operator_visible=True,
            requires_audit_trace=True,
            trace_id="trace_operator_intent_invalid",
            description="Invalid audit visibility entry.",
        )


def test_operator_audit_visibility_entry_rejects_invalid_state_class_pair() -> None:
    """Operator audit visibility entry should reject mismatched state/class pairs."""
    with pytest.raises(ValueError, match="audit_visibility_state and audit_event_class must remain semantically aligned."):
        OperatorAuditVisibilityEntry(
            audit_event_id="audit_visibility_invalid_pair",
            handoff_id="operator_handoff_003",
            operator_intent_id="operator_intent_003",
            audit_visibility_state="audit_visible_approval_bound",
            audit_event_class="read_only_navigation",
            operator_visible=True,
            requires_audit_trace=True,
            trace_id="trace_operator_intent_invalid_pair",
            description="Invalid audit visibility state/class pair.",
        )


def test_operator_audit_visibility_vocabularies_are_stable() -> None:
    """Operator audit visibility vocabularies should remain stable."""
    assert ALL_AUDIT_VISIBILITY_STATES == (
        "audit_visible_read_only",
        "audit_visible_approval_bound",
        "audit_visible_blocked",
        "audit_visible_failure",
    )
    assert ALL_AUDIT_EVENT_CLASSES == (
        "read_only_navigation",
        "approval_bound_control",
        "blocked_control",
        "failed_control",
    )

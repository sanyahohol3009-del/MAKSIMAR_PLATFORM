from __future__ import annotations

import pytest

from MAKSIMAR_CORE_LIB.oob_dashboard.operator_approval_decision_models import (
    ALL_APPROVAL_REQUIREMENTS,
    ALL_POLICY_DECISION_STATUSES,
    ALL_POLICY_REASON_CODES,
    OperatorApprovalDecisionEntry,
    build_operator_approval_decision_model,
)


def test_operator_approval_decision_model_builds() -> None:
    """Operator approval decision model should build successfully."""
    model = build_operator_approval_decision_model()

    assert model.model_id == "operator_approval_decision_model_001"
    assert model.total_entries == 3
    assert model.allowed_entries == 2
    assert model.blocked_entries == 0
    assert model.pending_approval_entries == 1
    assert model.deferred_entries == 0
    assert model.operator_visible_entries == 3


def test_operator_approval_decision_model_contains_expected_entries() -> None:
    """Operator approval decision model should contain expected canonical entries."""
    model = build_operator_approval_decision_model()
    entry_map = {entry.operator_intent_id: entry for entry in model.entries}

    view_entry = entry_map["operator_intent_001"]
    navigation_entry = entry_map["operator_intent_002"]
    control_entry = entry_map["operator_intent_003"]

    assert view_entry.policy_decision_status == "allowed"
    assert view_entry.approval_requirement == "no_approval_required"
    assert view_entry.reason_code == "operator_surface_allowed"
    assert view_entry.executable_after_approval is False

    assert navigation_entry.policy_decision_status == "allowed"
    assert navigation_entry.approval_requirement == "no_approval_required"

    assert control_entry.policy_decision_status == "pending_approval"
    assert control_entry.approval_requirement == "human_approval_required"
    assert control_entry.reason_code == "approval_required"
    assert control_entry.executable_after_approval is True


def test_operator_approval_decision_model_preserves_operator_visibility() -> None:
    """Operator approval decision model should preserve operator-visible explanations."""
    model = build_operator_approval_decision_model()

    for entry in model.entries:
        assert entry.explanation_visible_to_operator is True
        assert entry.trace_id.startswith("trace_operator_intent_")


def test_operator_approval_decision_entry_rejects_blank_id() -> None:
    """Operator approval decision entry should reject blank approval ids."""
    with pytest.raises(ValueError, match="approval_decision_id must be a non-empty string."):
        OperatorApprovalDecisionEntry(
            approval_decision_id="",
            operator_intent_id="operator_intent_001",
            policy_decision_status="allowed",
            approval_requirement="no_approval_required",
            reason_code="operator_surface_allowed",
            executable_after_approval=False,
            explanation_visible_to_operator=True,
            trace_id="trace_operator_intent_invalid",
            description="Invalid approval decision entry.",
        )


def test_operator_approval_decision_entry_rejects_unknown_policy_status() -> None:
    """Operator approval decision entry should reject unknown policy statuses."""
    with pytest.raises(ValueError, match="policy_decision_status must be one of"):
        OperatorApprovalDecisionEntry(
            approval_decision_id="operator_approval_decision_invalid_status",
            operator_intent_id="operator_intent_001",
            policy_decision_status="unknown_status",  # type: ignore[arg-type]
            approval_requirement="no_approval_required",
            reason_code="operator_surface_allowed",
            executable_after_approval=False,
            explanation_visible_to_operator=True,
            trace_id="trace_operator_intent_invalid_status",
            description="Invalid approval decision entry with unknown policy status.",
        )


def test_operator_approval_decision_entry_rejects_unknown_approval_requirement() -> None:
    """Operator approval decision entry should reject unknown approval requirements."""
    with pytest.raises(ValueError, match="approval_requirement must be one of"):
        OperatorApprovalDecisionEntry(
            approval_decision_id="operator_approval_decision_invalid_requirement",
            operator_intent_id="operator_intent_001",
            policy_decision_status="allowed",
            approval_requirement="unknown_requirement",  # type: ignore[arg-type]
            reason_code="operator_surface_allowed",
            executable_after_approval=False,
            explanation_visible_to_operator=True,
            trace_id="trace_operator_intent_invalid_requirement",
            description="Invalid approval decision entry with unknown approval requirement.",
        )


def test_operator_approval_decision_entry_rejects_unknown_reason_code() -> None:
    """Operator approval decision entry should reject unknown reason codes."""
    with pytest.raises(ValueError, match="reason_code must be one of"):
        OperatorApprovalDecisionEntry(
            approval_decision_id="operator_approval_decision_invalid_reason",
            operator_intent_id="operator_intent_001",
            policy_decision_status="allowed",
            approval_requirement="no_approval_required",
            reason_code="unknown_reason",  # type: ignore[arg-type]
            executable_after_approval=False,
            explanation_visible_to_operator=True,
            trace_id="trace_operator_intent_invalid_reason",
            description="Invalid approval decision entry with unknown reason code.",
        )


def test_operator_approval_decision_entry_rejects_allowed_status_with_approval_requirement() -> None:
    """Allowed decisions should not require approval."""
    with pytest.raises(ValueError, match="Allowed decisions must use no_approval_required."):
        OperatorApprovalDecisionEntry(
            approval_decision_id="operator_approval_decision_invalid_allowed",
            operator_intent_id="operator_intent_001",
            policy_decision_status="allowed",
            approval_requirement="human_approval_required",
            reason_code="operator_surface_allowed",
            executable_after_approval=False,
            explanation_visible_to_operator=True,
            trace_id="trace_operator_intent_invalid_allowed",
            description="Invalid allowed decision with approval requirement.",
        )


def test_operator_approval_decision_entry_rejects_blocked_executable_after_approval() -> None:
    """Blocked decisions cannot remain executable after approval."""
    with pytest.raises(ValueError, match="Blocked decisions cannot remain executable_after_approval."):
        OperatorApprovalDecisionEntry(
            approval_decision_id="operator_approval_decision_invalid_blocked",
            operator_intent_id="operator_intent_003",
            policy_decision_status="blocked",
            approval_requirement="human_approval_required",
            reason_code="restricted_panel",
            executable_after_approval=True,
            explanation_visible_to_operator=True,
            trace_id="trace_operator_intent_invalid_blocked",
            description="Invalid blocked decision marked executable after approval.",
        )


def test_operator_approval_decision_entry_rejects_pending_approval_without_requirement() -> None:
    """Pending approval decisions must carry an approval requirement."""
    with pytest.raises(ValueError, match="Pending approval decisions must require an approval mode."):
        OperatorApprovalDecisionEntry(
            approval_decision_id="operator_approval_decision_invalid_pending",
            operator_intent_id="operator_intent_003",
            policy_decision_status="pending_approval",
            approval_requirement="no_approval_required",
            reason_code="approval_required",
            executable_after_approval=True,
            explanation_visible_to_operator=True,
            trace_id="trace_operator_intent_invalid_pending",
            description="Invalid pending approval decision without approval requirement.",
        )


def test_operator_approval_decision_vocabularies_are_stable() -> None:
    """Operator approval decision vocabularies should remain stable."""
    assert ALL_APPROVAL_REQUIREMENTS == (
        "no_approval_required",
        "human_approval_required",
        "multi_factor_approval_required",
        "hardware_key_required",
    )
    assert ALL_POLICY_DECISION_STATUSES == (
        "allowed",
        "blocked",
        "pending_approval",
        "deferred",
    )
    assert ALL_POLICY_REASON_CODES == (
        "read_only_surface",
        "operator_surface_allowed",
        "approval_required",
        "restricted_panel",
        "forbidden_direct_execution",
        "unknown_action",
        "policy_hold",
    )

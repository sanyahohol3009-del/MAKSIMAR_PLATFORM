from __future__ import annotations

import pytest

from MAKSIMAR_CORE_LIB.oob_dashboard.operator_control_plane_handoff_models import (
    ALL_HANDOFF_STATES,
    CONTROL_PLANE_TARGETS,
    OperatorControlPlaneHandoffEntry,
    build_operator_control_plane_handoff_model,
)


def test_operator_control_plane_handoff_model_builds() -> None:
    """Operator control-plane handoff model should build successfully."""
    model = build_operator_control_plane_handoff_model()

    assert model.model_id == "operator_control_plane_handoff_model_001"
    assert model.total_entries == 3
    assert model.handoff_not_ready_entries == 2
    assert model.handoff_ready_entries == 1
    assert model.handoff_blocked_entries == 0
    assert model.handoff_emitted_entries == 0
    assert model.handoff_acknowledged_entries == 0
    assert model.handoff_failed_entries == 0


def test_operator_control_plane_handoff_model_contains_expected_entries() -> None:
    """Operator control-plane handoff model should contain expected canonical entries."""
    model = build_operator_control_plane_handoff_model()
    entry_map = {entry.operator_intent_id: entry for entry in model.entries}

    view_entry = entry_map["operator_intent_001"]
    navigation_entry = entry_map["operator_intent_002"]
    control_entry = entry_map["operator_intent_003"]

    assert view_entry.handoff_state == "handoff_not_ready"
    assert view_entry.control_plane_target == "control_plane_operator_router"
    assert view_entry.handoff_completed_at is None
    assert view_entry.handoff_denied_reason is None

    assert navigation_entry.handoff_state == "handoff_not_ready"
    assert navigation_entry.control_plane_target == "control_plane_operator_router"

    assert control_entry.handoff_state == "handoff_ready"
    assert control_entry.control_plane_target == "control_plane_policy_gate"
    assert control_entry.handoff_completed_at is None
    assert control_entry.handoff_denied_reason is None


def test_operator_control_plane_handoff_model_preserves_trace_visibility() -> None:
    """Operator control-plane handoff model should preserve trace visibility."""
    model = build_operator_control_plane_handoff_model()

    for entry in model.entries:
        assert entry.trace_id.startswith("trace_operator_intent_")
        assert entry.handoff_created_at == "runtime_unbound"


def test_operator_control_plane_handoff_entry_rejects_blank_id() -> None:
    """Operator control-plane handoff entry should reject blank handoff ids."""
    with pytest.raises(ValueError, match="handoff_id must be a non-empty string."):
        OperatorControlPlaneHandoffEntry(
            handoff_id="",
            operator_intent_id="operator_intent_001",
            control_plane_target="control_plane_operator_router",
            handoff_state="handoff_not_ready",
            handoff_created_at="runtime_unbound",
            handoff_completed_at=None,
            handoff_denied_reason=None,
            trace_id="trace_operator_intent_invalid",
            description="Invalid handoff entry.",
        )


def test_operator_control_plane_handoff_entry_rejects_unknown_handoff_state() -> None:
    """Operator control-plane handoff entry should reject unknown handoff states."""
    with pytest.raises(ValueError, match="handoff_state must be one of"):
        OperatorControlPlaneHandoffEntry(
            handoff_id="operator_handoff_invalid_state",
            operator_intent_id="operator_intent_001",
            control_plane_target="control_plane_operator_router",
            handoff_state="unknown_handoff_state",  # type: ignore[arg-type]
            handoff_created_at="runtime_unbound",
            handoff_completed_at=None,
            handoff_denied_reason=None,
            trace_id="trace_operator_intent_invalid_state",
            description="Invalid handoff entry with unknown handoff state.",
        )


def test_operator_control_plane_handoff_entry_rejects_unknown_control_plane_target() -> None:
    """Operator control-plane handoff entry should reject unknown control-plane targets."""
    with pytest.raises(ValueError, match="control_plane_target must be one of"):
        OperatorControlPlaneHandoffEntry(
            handoff_id="operator_handoff_invalid_target",
            operator_intent_id="operator_intent_001",
            control_plane_target="unknown_control_plane_target",
            handoff_state="handoff_not_ready",
            handoff_created_at="runtime_unbound",
            handoff_completed_at=None,
            handoff_denied_reason=None,
            trace_id="trace_operator_intent_invalid_target",
            description="Invalid handoff entry with unknown control-plane target.",
        )


def test_operator_control_plane_handoff_entry_requires_completion_time_for_acknowledged_state() -> None:
    """Acknowledged handoffs must include completion timestamps."""
    with pytest.raises(ValueError, match="handoff_acknowledged entries must include handoff_completed_at."):
        OperatorControlPlaneHandoffEntry(
            handoff_id="operator_handoff_invalid_acknowledged",
            operator_intent_id="operator_intent_003",
            control_plane_target="control_plane_execution_intake",
            handoff_state="handoff_acknowledged",
            handoff_created_at="runtime_unbound",
            handoff_completed_at=None,
            handoff_denied_reason=None,
            trace_id="trace_operator_intent_invalid_acknowledged",
            description="Invalid acknowledged handoff without completion time.",
        )


def test_operator_control_plane_handoff_entry_requires_denied_reason_for_failed_state() -> None:
    """Failed handoffs must include denied reasons."""
    with pytest.raises(ValueError, match="handoff_failed entries must include a non-empty handoff_denied_reason."):
        OperatorControlPlaneHandoffEntry(
            handoff_id="operator_handoff_invalid_failed",
            operator_intent_id="operator_intent_003",
            control_plane_target="control_plane_policy_gate",
            handoff_state="handoff_failed",
            handoff_created_at="runtime_unbound",
            handoff_completed_at=None,
            handoff_denied_reason=None,
            trace_id="trace_operator_intent_invalid_failed",
            description="Invalid failed handoff without denied reason.",
        )


def test_operator_control_plane_handoff_entry_rejects_denied_reason_on_non_failed_state() -> None:
    """Non-failed handoff states must not include denied reasons."""
    with pytest.raises(ValueError, match="Non-failed handoff states must not include handoff_denied_reason."):
        OperatorControlPlaneHandoffEntry(
            handoff_id="operator_handoff_invalid_denied_reason",
            operator_intent_id="operator_intent_003",
            control_plane_target="control_plane_policy_gate",
            handoff_state="handoff_ready",
            handoff_created_at="runtime_unbound",
            handoff_completed_at=None,
            handoff_denied_reason="unexpected_reason",
            trace_id="trace_operator_intent_invalid_denied_reason",
            description="Invalid non-failed handoff with denied reason.",
        )


def test_operator_control_plane_handoff_vocabularies_are_stable() -> None:
    """Operator control-plane handoff vocabularies should remain stable."""
    assert ALL_HANDOFF_STATES == (
        "handoff_not_ready",
        "handoff_ready",
        "handoff_blocked",
        "handoff_emitted",
        "handoff_acknowledged",
        "handoff_failed",
    )
    assert CONTROL_PLANE_TARGETS == (
        "control_plane_operator_router",
        "control_plane_policy_gate",
        "control_plane_execution_intake",
    )

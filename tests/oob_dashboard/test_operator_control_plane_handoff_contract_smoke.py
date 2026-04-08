from __future__ import annotations

import pytest

from MAKSIMAR_CORE_LIB.oob_dashboard.operator_control_plane_handoff_contract import (
    OperatorControlPlaneHandoffContractEntry,
    build_operator_control_plane_handoff_contract,
)


def test_operator_control_plane_handoff_contract_builds() -> None:
    """Operator control-plane handoff contract should build successfully."""
    contract = build_operator_control_plane_handoff_contract()

    assert contract.contract_id == "operator_control_plane_handoff_contract_001"
    assert contract.total_entries == 3
    assert contract.not_ready_entries == 2
    assert contract.ready_entries == 1
    assert contract.blocked_entries == 0
    assert contract.emitted_entries == 0
    assert contract.acknowledged_entries == 0
    assert contract.failed_entries == 0
    assert contract.operator_visible_entries == 3
    assert contract.baseline_aligned_entries == 3
    assert contract.structurally_valid_entries == 3


def test_operator_control_plane_handoff_contract_contains_expected_entries() -> None:
    """Operator control-plane handoff contract should contain expected canonical entries."""
    contract = build_operator_control_plane_handoff_contract()
    entry_map = {entry.operator_intent_id: entry for entry in contract.entries}

    view_entry = entry_map["operator_intent_001"]
    navigation_entry = entry_map["operator_intent_002"]
    control_entry = entry_map["operator_intent_003"]

    assert view_entry.handoff_state == "handoff_not_ready"
    assert view_entry.control_plane_target == "control_plane_operator_router"
    assert view_entry.baseline_family_aligned is True
    assert view_entry.structurally_valid is True

    assert navigation_entry.handoff_state == "handoff_not_ready"
    assert navigation_entry.control_plane_target == "control_plane_operator_router"
    assert navigation_entry.baseline_family_aligned is True

    assert control_entry.handoff_state == "handoff_ready"
    assert control_entry.control_plane_target == "control_plane_policy_gate"
    assert control_entry.baseline_family_aligned is True
    assert control_entry.operator_visible is True


def test_operator_control_plane_handoff_contract_preserves_trace_visibility() -> None:
    """Operator control-plane handoff contract should preserve trace visibility."""
    contract = build_operator_control_plane_handoff_contract()

    for entry in contract.entries:
        assert entry.trace_id.startswith("trace_operator_intent_")
        assert entry.target_registered is True
        assert entry.state_registered is True
        assert entry.structurally_valid is True


def test_operator_control_plane_handoff_contract_entry_rejects_blank_id() -> None:
    """Operator control-plane handoff contract entry should reject blank ids."""
    with pytest.raises(ValueError, match="handoff_id must be a non-empty string."):
        OperatorControlPlaneHandoffContractEntry(
            handoff_id="",
            operator_intent_id="operator_intent_001",
            control_plane_target="control_plane_operator_router",
            handoff_state="handoff_not_ready",
            handoff_created_at="runtime_unbound",
            handoff_completed_at=None,
            handoff_denied_reason=None,
            trace_id="trace_operator_intent_invalid",
            operator_visible=True,
            target_registered=True,
            state_registered=True,
            baseline_family_aligned=True,
            structurally_valid=True,
            description="Invalid contract entry.",
        )


def test_operator_control_plane_handoff_contract_entry_rejects_unknown_target() -> None:
    """Operator control-plane handoff contract entry should reject unknown targets."""
    with pytest.raises(ValueError, match="control_plane_target must be one of"):
        OperatorControlPlaneHandoffContractEntry(
            handoff_id="operator_handoff_contract_invalid_target",
            operator_intent_id="operator_intent_001",
            control_plane_target="unknown_target",
            handoff_state="handoff_not_ready",
            handoff_created_at="runtime_unbound",
            handoff_completed_at=None,
            handoff_denied_reason=None,
            trace_id="trace_operator_intent_invalid_target",
            operator_visible=True,
            target_registered=False,
            state_registered=True,
            baseline_family_aligned=False,
            structurally_valid=True,
            description="Invalid contract entry with unknown target.",
        )


def test_operator_control_plane_handoff_contract_entry_rejects_unknown_state() -> None:
    """Operator control-plane handoff contract entry should reject unknown states."""
    with pytest.raises(ValueError, match="handoff_state must be one of"):
        OperatorControlPlaneHandoffContractEntry(
            handoff_id="operator_handoff_contract_invalid_state",
            operator_intent_id="operator_intent_001",
            control_plane_target="control_plane_operator_router",
            handoff_state="unknown_state",
            handoff_created_at="runtime_unbound",
            handoff_completed_at=None,
            handoff_denied_reason=None,
            trace_id="trace_operator_intent_invalid_state",
            operator_visible=True,
            target_registered=True,
            state_registered=False,
            baseline_family_aligned=False,
            structurally_valid=True,
            description="Invalid contract entry with unknown state.",
        )


def test_operator_control_plane_handoff_contract_entry_requires_completion_timestamp_for_acknowledged_state() -> None:
    """Acknowledged contract entries must include completion timestamps."""
    with pytest.raises(ValueError, match="handoff_acknowledged entries must include handoff_completed_at."):
        OperatorControlPlaneHandoffContractEntry(
            handoff_id="operator_handoff_contract_invalid_ack",
            operator_intent_id="operator_intent_003",
            control_plane_target="control_plane_execution_intake",
            handoff_state="handoff_acknowledged",
            handoff_created_at="runtime_unbound",
            handoff_completed_at=None,
            handoff_denied_reason=None,
            trace_id="trace_operator_intent_invalid_ack",
            operator_visible=True,
            target_registered=True,
            state_registered=True,
            baseline_family_aligned=True,
            structurally_valid=True,
            description="Invalid acknowledged contract entry.",
        )


def test_operator_control_plane_handoff_contract_entry_requires_denied_reason_for_failed_state() -> None:
    """Failed contract entries must include denied reasons."""
    with pytest.raises(ValueError, match="handoff_failed entries must include a non-empty handoff_denied_reason."):
        OperatorControlPlaneHandoffContractEntry(
            handoff_id="operator_handoff_contract_invalid_failed",
            operator_intent_id="operator_intent_003",
            control_plane_target="control_plane_policy_gate",
            handoff_state="handoff_failed",
            handoff_created_at="runtime_unbound",
            handoff_completed_at=None,
            handoff_denied_reason=None,
            trace_id="trace_operator_intent_invalid_failed",
            operator_visible=True,
            target_registered=True,
            state_registered=True,
            baseline_family_aligned=True,
            structurally_valid=True,
            description="Invalid failed contract entry.",
        )


def test_operator_control_plane_handoff_contract_entry_requires_true_registration_flags() -> None:
    """Canonical contract entries must preserve registration flags."""
    with pytest.raises(ValueError, match="target_registered must be true"):
        OperatorControlPlaneHandoffContractEntry(
            handoff_id="operator_handoff_contract_invalid_registration",
            operator_intent_id="operator_intent_001",
            control_plane_target="control_plane_operator_router",
            handoff_state="handoff_not_ready",
            handoff_created_at="runtime_unbound",
            handoff_completed_at=None,
            handoff_denied_reason=None,
            trace_id="trace_operator_intent_invalid_registration",
            operator_visible=True,
            target_registered=False,
            state_registered=True,
            baseline_family_aligned=True,
            structurally_valid=True,
            description="Invalid registration flags.",
        )

from __future__ import annotations

import pytest

from MAKSIMAR_CORE_LIB.oob_dashboard.operator_interaction_read_model_contract import (
    OperatorInteractionReadModelEntry,
    build_operator_interaction_read_model_contract,
)


def test_operator_interaction_read_model_contract_builds() -> None:
    """Operator interaction read-model contract should build successfully."""
    contract = build_operator_interaction_read_model_contract()

    assert contract.contract_id == "operator_interaction_read_model_contract_001"
    assert contract.total_entries == 3
    assert contract.read_only_lane_entries == 2
    assert contract.approval_bound_lane_entries == 1
    assert contract.approval_required_entries == 1
    assert contract.handoff_ready_entries == 1
    assert contract.operator_visible_entries == 3


def test_operator_interaction_read_model_contains_expected_entries() -> None:
    """Operator interaction read-model should contain expected canonical entries."""
    contract = build_operator_interaction_read_model_contract()
    entry_map = {entry.operator_intent_id: entry for entry in contract.entries}

    assert entry_map["operator_intent_001"].interaction_lane == "read_only_lane"
    assert entry_map["operator_intent_001"].interaction_surface_state == "read_only_interaction_surface"
    assert entry_map["operator_intent_001"].handoff_ready is False

    assert entry_map["operator_intent_002"].interaction_lane == "read_only_lane"
    assert entry_map["operator_intent_002"].interaction_surface_state == "read_only_interaction_surface"

    assert entry_map["operator_intent_003"].interaction_lane == "approval_bound_lane"
    assert entry_map["operator_intent_003"].interaction_surface_state == "approval_bound_interaction_surface"
    assert entry_map["operator_intent_003"].handoff_ready is True


def test_operator_interaction_read_model_preserves_trace_visibility() -> None:
    """Operator interaction read-model should preserve trace visibility."""
    contract = build_operator_interaction_read_model_contract()

    for entry in contract.entries:
        assert entry.operator_visible is True
        assert entry.trace_id.startswith("trace_operator_intent_")


def test_operator_interaction_read_model_entry_rejects_blank_id() -> None:
    """Operator interaction read-model entry should reject blank ids."""
    with pytest.raises(ValueError, match="operator_intent_id must be a non-empty string."):
        OperatorInteractionReadModelEntry(
            operator_intent_id="",
            dashboard_id="dashboard_main_operator_001",
            workspace_id="workspace_operator_main",
            interaction_lane="read_only_lane",
            interaction_surface_state="read_only_interaction_surface",
            intent_kind="view_request",
            approval_state="approval_not_required",
            handoff_state="handoff_not_ready",
            audit_visibility_state="audit_visible_read_only",
            approval_required=False,
            handoff_ready=False,
            operator_visible=True,
            trace_id="trace_operator_intent_invalid",
            description="Invalid interaction read-model entry.",
        )


def test_operator_interaction_read_model_entry_rejects_approval_on_read_only_lane() -> None:
    """Read-only interaction lanes must not require approval."""
    with pytest.raises(ValueError, match="read_only_lane entries must not require approval."):
        OperatorInteractionReadModelEntry(
            operator_intent_id="operator_intent_invalid_lane",
            dashboard_id="dashboard_main_operator_001",
            workspace_id="workspace_operator_main",
            interaction_lane="read_only_lane",
            interaction_surface_state="read_only_interaction_surface",
            intent_kind="view_request",
            approval_state="approval_granted",
            handoff_state="handoff_ready",
            audit_visibility_state="audit_visible_read_only",
            approval_required=True,
            handoff_ready=True,
            operator_visible=True,
            trace_id="trace_operator_intent_invalid_lane",
            description="Invalid interaction lane approval mismatch.",
        )

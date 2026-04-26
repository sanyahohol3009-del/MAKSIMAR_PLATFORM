from __future__ import annotations

import pytest

from MAKSIMAR_CORE_LIB.oob_dashboard.operator_interaction_read_model_models import (
    OperatorInteractionReadModelContract,
    OperatorInteractionReadModelEntry,
)


def test_operator_interaction_read_model_entry_smoke() -> None:
    entry = OperatorInteractionReadModelEntry(
        operator_intent_id="intent_001",
        dashboard_id="main_operator_dashboard",
        workspace_id="workspace_operator_interaction",
        interaction_lane="approval_bound_lane",
        interaction_surface_state="approval_bound_interaction_surface",
        intent_kind="control_request",
        approval_state="approval_required",
        handoff_state="handoff_ready",
        audit_visibility_state="audit_visible_with_policy_and_approval",
        approval_required=True,
        handoff_ready=True,
        operator_visible=True,
        trace_id="trace_001",
        description="Read model description.",
    )

    assert entry.operator_intent_id == "intent_001"


def test_operator_interaction_read_model_entry_rejects_lane_mismatch() -> None:
    with pytest.raises(
        ValueError,
        match="read_only_lane entries must not require approval.",
    ):
        OperatorInteractionReadModelEntry(
            operator_intent_id="intent_001",
            dashboard_id="main_operator_dashboard",
            workspace_id="workspace_operator_interaction",
            interaction_lane="read_only_lane",
            interaction_surface_state="read_only_interaction_surface",
            intent_kind="view_request",
            approval_state="approval_required",
            handoff_state="handoff_ready",
            audit_visibility_state="audit_visible_with_policy_and_approval",
            approval_required=True,
            handoff_ready=True,
            operator_visible=True,
            trace_id="trace_001",
            description="Read model description.",
        )


def test_operator_interaction_read_model_contract_counts_match() -> None:
    entry = OperatorInteractionReadModelEntry(
        operator_intent_id="intent_001",
        dashboard_id="main_operator_dashboard",
        workspace_id="workspace_operator_interaction",
        interaction_lane="approval_bound_lane",
        interaction_surface_state="approval_bound_interaction_surface",
        intent_kind="control_request",
        approval_state="approval_required",
        handoff_state="handoff_ready",
        audit_visibility_state="audit_visible_with_policy_and_approval",
        approval_required=True,
        handoff_ready=True,
        operator_visible=True,
        trace_id="trace_001",
        description="Read model description.",
    )

    contract = OperatorInteractionReadModelContract(
        contract_id="operator_interaction_read_model_contract_001",
        total_entries=1,
        read_only_lane_entries=0,
        approval_bound_lane_entries=1,
        approval_required_entries=1,
        handoff_ready_entries=1,
        operator_visible_entries=1,
        entries=(entry,),
    )

    assert contract.total_entries == 1

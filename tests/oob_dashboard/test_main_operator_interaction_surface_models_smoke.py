from __future__ import annotations

import pytest

from MAKSIMAR_CORE_LIB.oob_dashboard.main_operator_interaction_surface_models import (
    MainOperatorInteractionSurfaceEntry,
)


def test_main_operator_interaction_surface_entry_accepts_read_only_surface() -> None:
    """Read-only interaction surfaces should validate successfully."""
    entry = MainOperatorInteractionSurfaceEntry(
        interaction_surface_id="main_operator_interaction_surface_001",
        operator_intent_id="operator_intent_001",
        dashboard_id="main_operator_dashboard",
        workspace_id="workspace_operator_main",
        surface_state="interaction_surface_ready",
        surface_class="read_only_surface",
        intent_kind="view_request",
        action_visible=True,
        disabled_state_visible=True,
        forbidden_state_visible=True,
        pending_approval_visible=False,
        approval_required=False,
        handoff_ready=True,
        audit_visible=True,
        operator_visible=True,
        trace_id="trace_operator_intent_001",
        description="Valid read-only interaction surface entry.",
    )

    assert entry.surface_class == "read_only_surface"
    assert entry.approval_required is False


def test_main_operator_interaction_surface_entry_accepts_approval_bound_surface() -> None:
    """Approval-bound interaction surfaces should validate successfully."""
    entry = MainOperatorInteractionSurfaceEntry(
        interaction_surface_id="main_operator_interaction_surface_002",
        operator_intent_id="operator_intent_003",
        dashboard_id="main_operator_dashboard",
        workspace_id="workspace_operator_main",
        surface_state="interaction_surface_ready",
        surface_class="approval_bound_surface",
        intent_kind="control_request",
        action_visible=True,
        disabled_state_visible=True,
        forbidden_state_visible=True,
        pending_approval_visible=True,
        approval_required=True,
        handoff_ready=True,
        audit_visible=True,
        operator_visible=True,
        trace_id="trace_operator_intent_003",
        description="Valid approval-bound interaction surface entry.",
    )

    assert entry.surface_class == "approval_bound_surface"
    assert entry.approval_required is True


def test_main_operator_interaction_surface_entry_rejects_missing_pending_approval_visibility() -> None:
    """Approval-bound surfaces must expose pending approval visibility."""
    with pytest.raises(
        ValueError,
        match="approval_bound_surface entries must expose pending_approval_visible=True.",
    ):
        MainOperatorInteractionSurfaceEntry(
            interaction_surface_id="main_operator_interaction_surface_003",
            operator_intent_id="operator_intent_003",
            dashboard_id="main_operator_dashboard",
            workspace_id="workspace_operator_main",
            surface_state="interaction_surface_ready",
            surface_class="approval_bound_surface",
            intent_kind="control_request",
            action_visible=True,
            disabled_state_visible=True,
            forbidden_state_visible=True,
            pending_approval_visible=False,
            approval_required=True,
            handoff_ready=True,
            audit_visible=True,
            operator_visible=True,
            trace_id="trace_operator_intent_003",
            description="Invalid approval-bound interaction surface entry.",
        )

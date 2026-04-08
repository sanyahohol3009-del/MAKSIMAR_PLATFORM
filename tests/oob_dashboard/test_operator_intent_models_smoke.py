from __future__ import annotations

import pytest

from MAKSIMAR_CORE_LIB.oob_dashboard.operator_intent_models import (
    ALL_INTENT_KINDS,
    ALL_INTENT_STATES,
    ALL_REQUESTED_ACTION_KINDS,
    OperatorIntentEntry,
    build_operator_intent_model,
)


def test_operator_intent_model_builds() -> None:
    """Operator intent model should build successfully."""
    model = build_operator_intent_model()

    assert model.model_id == "operator_intent_model_001"
    assert model.total_entries == 3
    assert model.approval_required_entries == 1
    assert model.unique_panels == 3
    assert len(model.entries) == 3


def test_operator_intent_model_contains_expected_canonical_entries() -> None:
    """Operator intent model should expose canonical baseline entries."""
    model = build_operator_intent_model()

    assert model.entries[0].operator_intent_id == "operator_intent_001"
    assert model.entries[0].panel_id == "panel_chat"
    assert model.entries[0].intent_kind == "view_request"
    assert model.entries[0].requested_action == "view_panel"
    assert model.entries[0].intent_state == "intent_created"

    assert model.entries[1].operator_intent_id == "operator_intent_002"
    assert model.entries[1].panel_id == "panel_settings"
    assert model.entries[1].intent_kind == "navigation_request"
    assert model.entries[1].requested_action == "navigate_workspace"
    assert model.entries[1].intent_state == "intent_validated"

    assert model.entries[2].operator_intent_id == "operator_intent_003"
    assert model.entries[2].panel_id == "panel_gesture_control"
    assert model.entries[2].intent_kind == "control_request"
    assert model.entries[2].requested_action == "request_control_surface"
    assert model.entries[2].intent_state == "intent_pending_approval"


def test_operator_intent_model_preserves_operator_surface_coordinates() -> None:
    """Operator intent model should preserve canonical workspace and display targets."""
    model = build_operator_intent_model()

    for entry in model.entries:
        assert entry.workspace_id == "workspace_operator_main"
        assert entry.display_target_id == "display_primary_operator"
        assert entry.requested_by == "operator_primary"
        assert entry.requested_at == "runtime_unbound"
        assert entry.trace_id.startswith("trace_operator_intent_")


def test_operator_intent_model_tracks_approval_required_entries() -> None:
    """Operator intent model should track approval-required entries correctly."""
    model = build_operator_intent_model()

    approval_required_entries = [
        entry for entry in model.entries if entry.approval_required
    ]

    assert len(approval_required_entries) == 1
    assert approval_required_entries[0].panel_id == "panel_gesture_control"
    assert approval_required_entries[0].intent_state == "intent_pending_approval"


def test_operator_intent_entry_rejects_blank_identity_fields() -> None:
    """Operator intent entry should reject blank required identity fields."""
    with pytest.raises(ValueError, match="operator_intent_id must be a non-empty string."):
        OperatorIntentEntry(
            operator_intent_id="",
            panel_id="panel_chat",
            workspace_id="workspace_operator_main",
            display_target_id="display_primary_operator",
            intent_kind="view_request",
            requested_action="view_panel",
            intent_state="intent_created",
            requested_by="operator_primary",
            requested_at="runtime_unbound",
            approval_required=False,
            trace_id="trace_operator_intent_invalid",
            description="Invalid entry with blank operator intent id.",
        )


def test_operator_intent_entry_rejects_unknown_intent_kind() -> None:
    """Operator intent entry should reject unknown intent kinds."""
    with pytest.raises(ValueError, match="intent_kind must be one of"):
        OperatorIntentEntry(
            operator_intent_id="operator_intent_invalid_kind",
            panel_id="panel_chat",
            workspace_id="workspace_operator_main",
            display_target_id="display_primary_operator",
            intent_kind="unknown_intent_kind",  # type: ignore[arg-type]
            requested_action="view_panel",
            intent_state="intent_created",
            requested_by="operator_primary",
            requested_at="runtime_unbound",
            approval_required=False,
            trace_id="trace_operator_intent_invalid_kind",
            description="Invalid entry with unknown intent kind.",
        )


def test_operator_intent_entry_rejects_unknown_intent_state() -> None:
    """Operator intent entry should reject unknown intent states."""
    with pytest.raises(ValueError, match="intent_state must be one of"):
        OperatorIntentEntry(
            operator_intent_id="operator_intent_invalid_state",
            panel_id="panel_chat",
            workspace_id="workspace_operator_main",
            display_target_id="display_primary_operator",
            intent_kind="view_request",
            requested_action="view_panel",
            intent_state="unknown_intent_state",  # type: ignore[arg-type]
            requested_by="operator_primary",
            requested_at="runtime_unbound",
            approval_required=False,
            trace_id="trace_operator_intent_invalid_state",
            description="Invalid entry with unknown intent state.",
        )


def test_operator_intent_entry_rejects_unknown_requested_action() -> None:
    """Operator intent entry should reject unknown requested actions."""
    with pytest.raises(ValueError, match="requested_action must be one of"):
        OperatorIntentEntry(
            operator_intent_id="operator_intent_invalid_action",
            panel_id="panel_chat",
            workspace_id="workspace_operator_main",
            display_target_id="display_primary_operator",
            intent_kind="view_request",
            requested_action="unknown_requested_action",  # type: ignore[arg-type]
            intent_state="intent_created",
            requested_by="operator_primary",
            requested_at="runtime_unbound",
            approval_required=False,
            trace_id="trace_operator_intent_invalid_action",
            description="Invalid entry with unknown requested action.",
        )


def test_operator_intent_vocabularies_are_stable() -> None:
    """Operator intent vocabularies should remain stable and explicit."""
    assert ALL_INTENT_KINDS == (
        "view_request",
        "navigation_request",
        "control_request",
        "approval_request",
        "system_action_request",
    )
    assert ALL_INTENT_STATES == (
        "intent_created",
        "intent_validated",
        "intent_blocked",
        "intent_pending_approval",
        "intent_approved",
        "intent_rejected",
        "intent_handoff_ready",
        "intent_handed_off",
    )
    assert ALL_REQUESTED_ACTION_KINDS == (
        "view_panel",
        "navigate_workspace",
        "request_control_surface",
        "request_approval_flow",
        "request_system_action",
    )

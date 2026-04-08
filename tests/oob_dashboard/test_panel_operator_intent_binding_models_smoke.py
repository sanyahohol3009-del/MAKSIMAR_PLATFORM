from __future__ import annotations

import pytest

from MAKSIMAR_CORE_LIB.oob_dashboard.panel_operator_intent_binding_models import (
    PanelOperatorIntentBindingEntry,
    build_panel_operator_intent_binding_model,
)


def test_panel_operator_intent_binding_model_builds() -> None:
    """Panel operator intent binding model should build successfully."""
    model = build_panel_operator_intent_binding_model()

    assert model.model_id == "panel_operator_intent_binding_model_001"
    assert model.total_entries == 7
    assert model.interactive_entries == 4
    assert model.approval_bound_entries == 1
    assert model.read_only_fallback_entries == 4
    assert len(model.entries) == 7


def test_panel_operator_intent_binding_model_contains_expected_foundation_entries() -> None:
    """Panel operator intent binding model should contain expected foundation entries."""
    model = build_panel_operator_intent_binding_model()
    entry_map = {entry.panel_id: entry for entry in model.entries}

    assert entry_map["panel_consistency"].workspace_id == "workspace_foundation_monitoring"
    assert entry_map["panel_consistency"].display_target_id == "display_secondary_diagnostics"
    assert entry_map["panel_consistency"].allowed_intent_kinds == ("view_request",)
    assert entry_map["panel_consistency"].interactive is False

    assert entry_map["panel_snapshot"].allowed_intent_kinds == ("view_request",)
    assert entry_map["panel_incident"].allowed_intent_kinds == ("view_request",)


def test_panel_operator_intent_binding_model_contains_expected_operator_entries() -> None:
    """Panel operator intent binding model should contain expected operator entries."""
    model = build_panel_operator_intent_binding_model()
    entry_map = {entry.panel_id: entry for entry in model.entries}

    assert entry_map["panel_chat"].workspace_id == "workspace_operator_main"
    assert entry_map["panel_chat"].display_target_id == "display_primary_operator"
    assert entry_map["panel_chat"].allowed_intent_kinds == (
        "view_request",
        "navigation_request",
        "approval_request",
    )
    assert entry_map["panel_chat"].interactive is True
    assert entry_map["panel_chat"].read_only_fallback is True

    assert entry_map["panel_settings"].allowed_intent_kinds == (
        "view_request",
        "navigation_request",
    )

    assert entry_map["panel_gesture_control"].allowed_intent_kinds == (
        "view_request",
        "control_request",
        "approval_request",
    )
    assert entry_map["panel_gesture_control"].requires_explicit_approval is True


def test_panel_operator_intent_binding_model_preserves_non_executing_panel_semantics() -> None:
    """Panel operator intent bindings should preserve non-executing semantics."""
    model = build_panel_operator_intent_binding_model()

    for entry in model.entries:
        assert "system_action_request" not in entry.allowed_intent_kinds

    gesture_entry = next(
        entry for entry in model.entries if entry.panel_id == "panel_gesture_control"
    )
    assert gesture_entry.requires_explicit_approval is True
    assert gesture_entry.read_only_fallback is True


def test_panel_operator_intent_binding_entry_rejects_blank_binding_id() -> None:
    """Panel operator intent binding entry should reject blank binding ids."""
    with pytest.raises(ValueError, match="binding_id must be a non-empty string."):
        PanelOperatorIntentBindingEntry(
            binding_id="",
            panel_id="panel_chat",
            workspace_id="workspace_operator_main",
            display_target_id="display_primary_operator",
            allowed_intent_kinds=("view_request",),
            requires_explicit_approval=False,
            interactive=True,
            read_only_fallback=True,
            description="Invalid binding entry.",
        )


def test_panel_operator_intent_binding_entry_rejects_empty_intent_kind_tuple() -> None:
    """Panel operator intent binding entry should reject empty intent kind tuples."""
    with pytest.raises(ValueError, match="allowed_intent_kinds must contain at least one value."):
        PanelOperatorIntentBindingEntry(
            binding_id="panel_operator_intent_binding_invalid",
            panel_id="panel_chat",
            workspace_id="workspace_operator_main",
            display_target_id="display_primary_operator",
            allowed_intent_kinds=(),
            requires_explicit_approval=False,
            interactive=True,
            read_only_fallback=True,
            description="Invalid binding entry with empty intent kinds.",
        )


def test_panel_operator_intent_binding_entry_rejects_unknown_intent_kind() -> None:
    """Panel operator intent binding entry should reject unknown intent kinds."""
    with pytest.raises(ValueError, match="allowed_intent_kinds must only contain canonical intent kinds."):
        PanelOperatorIntentBindingEntry(
            binding_id="panel_operator_intent_binding_invalid_kind",
            panel_id="panel_chat",
            workspace_id="workspace_operator_main",
            display_target_id="display_primary_operator",
            allowed_intent_kinds=("view_request", "unknown_intent_kind"),  # type: ignore[arg-type]
            requires_explicit_approval=False,
            interactive=True,
            read_only_fallback=True,
            description="Invalid binding entry with unknown intent kind.",
        )


def test_panel_operator_intent_binding_entry_rejects_read_only_fallback_on_non_interactive_panel() -> None:
    """Panel operator intent binding entry should reject read-only fallback on non-interactive panels."""
    with pytest.raises(ValueError, match="read_only_fallback may only be true for interactive panels."):
        PanelOperatorIntentBindingEntry(
            binding_id="panel_operator_intent_binding_invalid_fallback",
            panel_id="panel_consistency",
            workspace_id="workspace_foundation_monitoring",
            display_target_id="display_secondary_diagnostics",
            allowed_intent_kinds=("view_request",),
            requires_explicit_approval=False,
            interactive=False,
            read_only_fallback=True,
            description="Invalid binding entry with impossible fallback configuration.",
        )

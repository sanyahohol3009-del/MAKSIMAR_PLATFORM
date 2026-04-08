from __future__ import annotations

from dataclasses import dataclass

from MAKSIMAR_CORE_LIB.oob_dashboard.operator_intent_models import (
    ALL_INTENT_KINDS,
    IntentKind,
)


def _require_non_empty(value: str, field_name: str) -> None:
    """Validate that a string field is present and not blank."""
    if not value or not value.strip():
        raise ValueError(f"{field_name} must be a non-empty string.")


def _require_non_empty_tuple(values: tuple[str, ...], field_name: str) -> None:
    """Validate that a tuple is present and all values are non-empty."""
    if not values:
        raise ValueError(f"{field_name} must contain at least one value.")
    for value in values:
        if not value or not value.strip():
            raise ValueError(f"{field_name} must not contain blank values.")


@dataclass(frozen=True, slots=True)
class PanelOperatorIntentBindingEntry:
    """Canonical panel-to-operator-intent binding entry.

    This model declares which operator intent kinds a given panel may originate
    inside a specific workspace/display context. The entry is descriptive and
    policy-aligned; it does not grant execution privileges.
    """

    binding_id: str
    panel_id: str
    workspace_id: str
    display_target_id: str
    allowed_intent_kinds: tuple[IntentKind, ...]
    requires_explicit_approval: bool
    interactive: bool
    read_only_fallback: bool
    description: str

    def __post_init__(self) -> None:
        """Validate canonical panel operator intent binding entry fields."""
        _require_non_empty(self.binding_id, "binding_id")
        _require_non_empty(self.panel_id, "panel_id")
        _require_non_empty(self.workspace_id, "workspace_id")
        _require_non_empty(self.display_target_id, "display_target_id")
        _require_non_empty(self.description, "description")
        _require_non_empty_tuple(self.allowed_intent_kinds, "allowed_intent_kinds")

        for intent_kind in self.allowed_intent_kinds:
            if intent_kind not in ALL_INTENT_KINDS:
                raise ValueError(
                    "allowed_intent_kinds must only contain canonical intent kinds. "
                    f"Got {intent_kind!r}, expected one of {ALL_INTENT_KINDS}."
                )

        if self.read_only_fallback and not self.interactive:
            raise ValueError(
                "read_only_fallback may only be true for interactive panels."
            )


@dataclass(frozen=True, slots=True)
class PanelOperatorIntentBindingModel:
    """Canonical panel-to-operator-intent binding model."""

    model_id: str
    total_entries: int
    interactive_entries: int
    approval_bound_entries: int
    read_only_fallback_entries: int
    entries: tuple[PanelOperatorIntentBindingEntry, ...]

    def __post_init__(self) -> None:
        """Validate canonical panel operator intent binding model fields."""
        _require_non_empty(self.model_id, "model_id")

        if self.total_entries != len(self.entries):
            raise ValueError(
                "total_entries must match the number of entries in the model."
            )

        if self.interactive_entries != sum(
            1 for entry in self.entries if entry.interactive
        ):
            raise ValueError(
                "interactive_entries must match interactive entry count."
            )

        if self.approval_bound_entries != sum(
            1 for entry in self.entries if entry.requires_explicit_approval
        ):
            raise ValueError(
                "approval_bound_entries must match approval-bound entry count."
            )

        if self.read_only_fallback_entries != sum(
            1 for entry in self.entries if entry.read_only_fallback
        ):
            raise ValueError(
                "read_only_fallback_entries must match read-only fallback entry count."
            )


def build_panel_operator_intent_binding_model() -> PanelOperatorIntentBindingModel:
    """Build canonical panel-to-operator-intent binding model."""

    entries = (
        PanelOperatorIntentBindingEntry(
            binding_id="panel_operator_intent_binding_001",
            panel_id="panel_consistency",
            workspace_id="workspace_foundation_monitoring",
            display_target_id="display_secondary_diagnostics",
            allowed_intent_kinds=("view_request",),
            requires_explicit_approval=False,
            interactive=False,
            read_only_fallback=False,
            description=(
                "Canonical binding for the consistency panel as a read-only "
                "foundation monitoring surface."
            ),
        ),
        PanelOperatorIntentBindingEntry(
            binding_id="panel_operator_intent_binding_002",
            panel_id="panel_snapshot",
            workspace_id="workspace_foundation_monitoring",
            display_target_id="display_secondary_diagnostics",
            allowed_intent_kinds=("view_request",),
            requires_explicit_approval=False,
            interactive=False,
            read_only_fallback=False,
            description=(
                "Canonical binding for the snapshot panel as a read-only "
                "foundation monitoring surface."
            ),
        ),
        PanelOperatorIntentBindingEntry(
            binding_id="panel_operator_intent_binding_003",
            panel_id="panel_incident",
            workspace_id="workspace_foundation_monitoring",
            display_target_id="display_secondary_diagnostics",
            allowed_intent_kinds=("view_request",),
            requires_explicit_approval=False,
            interactive=False,
            read_only_fallback=False,
            description=(
                "Canonical binding for the incident panel as a read-only "
                "diagnostics surface."
            ),
        ),
        PanelOperatorIntentBindingEntry(
            binding_id="panel_operator_intent_binding_004",
            panel_id="panel_diagnostics",
            workspace_id="workspace_expansion_observability",
            display_target_id="display_tertiary_expansion",
            allowed_intent_kinds=("view_request", "navigation_request"),
            requires_explicit_approval=False,
            interactive=True,
            read_only_fallback=True,
            description=(
                "Canonical binding for the diagnostics panel with controlled "
                "navigation visibility and read-only fallback."
            ),
        ),
        PanelOperatorIntentBindingEntry(
            binding_id="panel_operator_intent_binding_005",
            panel_id="panel_chat",
            workspace_id="workspace_operator_main",
            display_target_id="display_primary_operator",
            allowed_intent_kinds=("view_request", "navigation_request", "approval_request"),
            requires_explicit_approval=False,
            interactive=True,
            read_only_fallback=True,
            description=(
                "Canonical binding for the chat panel with operator-visible "
                "interaction surfaces that remain non-executing."
            ),
        ),
        PanelOperatorIntentBindingEntry(
            binding_id="panel_operator_intent_binding_006",
            panel_id="panel_settings",
            workspace_id="workspace_operator_main",
            display_target_id="display_primary_operator",
            allowed_intent_kinds=("view_request", "navigation_request"),
            requires_explicit_approval=False,
            interactive=True,
            read_only_fallback=True,
            description=(
                "Canonical binding for the settings panel with controlled "
                "operator navigation and read-only fallback."
            ),
        ),
        PanelOperatorIntentBindingEntry(
            binding_id="panel_operator_intent_binding_007",
            panel_id="panel_gesture_control",
            workspace_id="workspace_operator_main",
            display_target_id="display_primary_operator",
            allowed_intent_kinds=("view_request", "control_request", "approval_request"),
            requires_explicit_approval=True,
            interactive=True,
            read_only_fallback=True,
            description=(
                "Canonical binding for the gesture control panel where control "
                "requests remain approval-bound and never direct-executing."
            ),
        ),
    )

    return PanelOperatorIntentBindingModel(
        model_id="panel_operator_intent_binding_model_001",
        total_entries=len(entries),
        interactive_entries=sum(1 for entry in entries if entry.interactive),
        approval_bound_entries=sum(
            1 for entry in entries if entry.requires_explicit_approval
        ),
        read_only_fallback_entries=sum(
            1 for entry in entries if entry.read_only_fallback
        ),
        entries=entries,
    )

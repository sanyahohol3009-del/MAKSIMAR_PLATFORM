from __future__ import annotations

from dataclasses import dataclass


def _require_non_empty(value: str, field_name: str) -> None:
    if not value or not value.strip():
        raise ValueError(f"{field_name} must be a non-empty string.")


@dataclass(frozen=True, slots=True)
class PanelOperatorIntentBindingContractEntry:
    """Canonical panel-operator intent binding entry."""

    binding_id: str
    panel_id: str
    workspace_id: str
    display_target_id: str
    operator_intent_id: str
    allowed_intent_kinds: tuple[str, ...]
    interactive: bool
    panel_registered: bool
    workspace_registered: bool
    display_target_registered: bool
    structurally_valid: bool
    direct_execution_allowed: bool
    approval_required: bool
    requires_explicit_approval: bool
    read_only_fallback: bool
    fallback_safe: bool
    description: str

    def __post_init__(self) -> None:
        _require_non_empty(self.binding_id, "binding_id")
        _require_non_empty(self.panel_id, "panel_id")
        _require_non_empty(self.workspace_id, "workspace_id")
        _require_non_empty(self.display_target_id, "display_target_id")
        _require_non_empty(self.operator_intent_id, "operator_intent_id")
        _require_non_empty(self.description, "description")

        if not self.allowed_intent_kinds:
            raise ValueError("allowed_intent_kinds must be non-empty.")

        for intent_kind in self.allowed_intent_kinds:
            _require_non_empty(intent_kind, "allowed_intent_kinds item")


@dataclass(frozen=True, slots=True)
class PanelOperatorIntentBindingContract:
    """Canonical panel-operator intent binding contract."""

    contract_id: str
    total_entries: int
    structurally_valid_entries: int
    interactive_entries: int
    approval_bound_entries: int
    read_only_fallback_entries: int
    entries: tuple[PanelOperatorIntentBindingContractEntry, ...]

    def __post_init__(self) -> None:
        _require_non_empty(self.contract_id, "contract_id")

        if self.total_entries != len(self.entries):
            raise ValueError("total_entries must match len(entries).")

        if self.structurally_valid_entries != sum(
            1 for entry in self.entries if entry.structurally_valid
        ):
            raise ValueError(
                "structurally_valid_entries must match structurally_valid count."
            )

        if self.interactive_entries != sum(
            1 for entry in self.entries if entry.interactive
        ):
            raise ValueError("interactive_entries must match interactive count.")

        if self.approval_bound_entries != sum(
            1 for entry in self.entries if entry.approval_required
        ):
            raise ValueError(
                "approval_bound_entries must match approval_required count."
            )

        if self.read_only_fallback_entries != sum(
            1 for entry in self.entries if entry.read_only_fallback
        ):
            raise ValueError(
                "read_only_fallback_entries must match read_only_fallback count."
            )


def build_panel_operator_intent_binding_contract() -> PanelOperatorIntentBindingContract:
    """Build canonical panel-operator intent binding contract."""
    entries = (
        PanelOperatorIntentBindingContractEntry(
            binding_id="panel_operator_intent_binding_001",
            panel_id="panel_consistency",
            workspace_id="workspace_foundation_monitoring",
            display_target_id="display_secondary_diagnostics",
            operator_intent_id="intent_open_consistency",
            allowed_intent_kinds=("view_request",),
            interactive=False,
            panel_registered=True,
            workspace_registered=True,
            display_target_registered=True,
            structurally_valid=True,
            direct_execution_allowed=False,
            approval_required=False,
            requires_explicit_approval=False,
            read_only_fallback=False,
            fallback_safe=True,
            description="Canonical binding for consistency panel.",
        ),
        PanelOperatorIntentBindingContractEntry(
            binding_id="panel_operator_intent_binding_002",
            panel_id="panel_snapshot",
            workspace_id="workspace_foundation_monitoring",
            display_target_id="display_primary_operator",
            operator_intent_id="intent_open_snapshot",
            allowed_intent_kinds=("view_request",),
            interactive=False,
            panel_registered=True,
            workspace_registered=True,
            display_target_registered=True,
            structurally_valid=True,
            direct_execution_allowed=False,
            approval_required=False,
            requires_explicit_approval=False,
            read_only_fallback=False,
            fallback_safe=True,
            description="Canonical binding for snapshot panel.",
        ),
        PanelOperatorIntentBindingContractEntry(
            binding_id="panel_operator_intent_binding_003",
            panel_id="panel_incident",
            workspace_id="workspace_foundation_monitoring",
            display_target_id="display_secondary_diagnostics",
            operator_intent_id="intent_open_incident",
            allowed_intent_kinds=("view_request",),
            interactive=False,
            panel_registered=True,
            workspace_registered=True,
            display_target_registered=True,
            structurally_valid=True,
            direct_execution_allowed=False,
            approval_required=False,
            requires_explicit_approval=False,
            read_only_fallback=False,
            fallback_safe=True,
            description="Canonical binding for incident panel.",
        ),
        PanelOperatorIntentBindingContractEntry(
            binding_id="panel_operator_intent_binding_004",
            panel_id="panel_diagnostics",
            workspace_id="workspace_expansion_observability",
            display_target_id="display_tertiary_expansion",
            operator_intent_id="intent_open_diagnostics",
            allowed_intent_kinds=(
                "view_request",
                "navigation_request",
            ),
            interactive=True,
            panel_registered=True,
            workspace_registered=True,
            display_target_registered=True,
            structurally_valid=True,
            direct_execution_allowed=False,
            approval_required=False,
            requires_explicit_approval=False,
            read_only_fallback=True,
            fallback_safe=True,
            description="Canonical binding for diagnostics panel.",
        ),
        PanelOperatorIntentBindingContractEntry(
            binding_id="panel_operator_intent_binding_005",
            panel_id="panel_chat",
            workspace_id="workspace_operator_main",
            display_target_id="display_primary_operator",
            operator_intent_id="intent_open_chat",
            allowed_intent_kinds=(
                "view_request",
                "navigation_request",
                "approval_request",
            ),
            interactive=True,
            panel_registered=True,
            workspace_registered=True,
            display_target_registered=True,
            structurally_valid=True,
            direct_execution_allowed=False,
            approval_required=False,
            requires_explicit_approval=False,
            read_only_fallback=True,
            fallback_safe=True,
            description="Canonical binding for chat panel.",
        ),
        PanelOperatorIntentBindingContractEntry(
            binding_id="panel_operator_intent_binding_006",
            panel_id="panel_settings",
            workspace_id="workspace_operator_main",
            display_target_id="display_primary_operator",
            operator_intent_id="intent_open_settings",
            allowed_intent_kinds=(
                "view_request",
                "navigation_request",
            ),
            interactive=True,
            panel_registered=True,
            workspace_registered=True,
            display_target_registered=True,
            structurally_valid=True,
            direct_execution_allowed=False,
            approval_required=True,
            requires_explicit_approval=True,
            read_only_fallback=True,
            fallback_safe=True,
            description="Canonical binding for settings panel.",
        ),
        PanelOperatorIntentBindingContractEntry(
            binding_id="panel_operator_intent_binding_007",
            panel_id="panel_gesture_control",
            workspace_id="workspace_operator_main",
            display_target_id="display_primary_operator",
            operator_intent_id="intent_open_gesture_control",
            allowed_intent_kinds=(
                "view_request",
                "control_request",
                "approval_request",
            ),
            interactive=True,
            panel_registered=True,
            workspace_registered=True,
            display_target_registered=True,
            structurally_valid=True,
            direct_execution_allowed=False,
            approval_required=False,
            requires_explicit_approval=True,
            read_only_fallback=True,
            fallback_safe=True,
            description="Canonical binding for gesture control panel.",
        ),
    )

    return PanelOperatorIntentBindingContract(
        contract_id="panel_operator_intent_binding_contract_001",
        total_entries=len(entries),
        structurally_valid_entries=sum(
            1 for entry in entries if entry.structurally_valid
        ),
        interactive_entries=sum(
            1 for entry in entries if entry.interactive
        ),
        approval_bound_entries=sum(
            1 for entry in entries if entry.approval_required
        ),
        read_only_fallback_entries=sum(
            1 for entry in entries if entry.read_only_fallback
        ),
        entries=entries,
    )

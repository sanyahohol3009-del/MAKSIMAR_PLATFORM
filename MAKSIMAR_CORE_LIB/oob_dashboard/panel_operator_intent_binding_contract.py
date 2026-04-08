from __future__ import annotations

from dataclasses import dataclass

from MAKSIMAR_CORE_LIB.oob_dashboard.display_target_vocabulary_contract import (
    build_display_target_vocabulary_contract,
)
from MAKSIMAR_CORE_LIB.oob_dashboard.panel_operator_intent_binding_models import (
    build_panel_operator_intent_binding_model,
)
from MAKSIMAR_CORE_LIB.oob_dashboard.panel_registry_contract import (
    build_dashboard_panel_registry_contract,
)
from MAKSIMAR_CORE_LIB.oob_dashboard.workspace_registry_contract import (
    build_workspace_registry_contract,
)


@dataclass(frozen=True, slots=True)
class PanelOperatorIntentBindingContractEntry:
    """Canonical panel operator intent binding contract entry."""

    binding_id: str
    panel_id: str
    workspace_id: str
    display_target_id: str
    allowed_intent_kinds: tuple[str, ...]
    requires_explicit_approval: bool
    interactive: bool
    read_only_fallback: bool
    panel_registered: bool
    workspace_registered: bool
    display_target_registered: bool
    structurally_valid: bool
    description: str


@dataclass(frozen=True, slots=True)
class PanelOperatorIntentBindingContract:
    """Canonical panel operator intent binding contract."""

    contract_id: str
    total_entries: int
    structurally_valid_entries: int
    interactive_entries: int
    approval_bound_entries: int
    read_only_fallback_entries: int
    entries: tuple[PanelOperatorIntentBindingContractEntry, ...]


def build_panel_operator_intent_binding_contract() -> PanelOperatorIntentBindingContract:
    """Build canonical panel operator intent binding contract."""
    model = build_panel_operator_intent_binding_model()
    panel_registry = build_dashboard_panel_registry_contract()
    workspace_registry = build_workspace_registry_contract()
    display_contract = build_display_target_vocabulary_contract()

    registered_panel_ids = {entry.panel_id for entry in panel_registry.panels}
    registered_workspace_ids = {
        entry.workspace_id for entry in workspace_registry.entries
    }
    registered_display_target_ids = {
        entry.display_target_id for entry in display_contract.entries
    }

    entries = tuple(
        PanelOperatorIntentBindingContractEntry(
            binding_id=entry.binding_id,
            panel_id=entry.panel_id,
            workspace_id=entry.workspace_id,
            display_target_id=entry.display_target_id,
            allowed_intent_kinds=entry.allowed_intent_kinds,
            requires_explicit_approval=entry.requires_explicit_approval,
            interactive=entry.interactive,
            read_only_fallback=entry.read_only_fallback,
            panel_registered=entry.panel_id in registered_panel_ids,
            workspace_registered=entry.workspace_id in registered_workspace_ids,
            display_target_registered=(
                entry.display_target_id in registered_display_target_ids
            ),
            structurally_valid=(
                entry.panel_id in registered_panel_ids
                and entry.workspace_id in registered_workspace_ids
                and entry.display_target_id in registered_display_target_ids
            ),
            description=entry.description,
        )
        for entry in model.entries
    )

    return PanelOperatorIntentBindingContract(
        contract_id="panel_operator_intent_binding_contract_001",
        total_entries=len(entries),
        structurally_valid_entries=sum(
            1 for entry in entries if entry.structurally_valid
        ),
        interactive_entries=sum(1 for entry in entries if entry.interactive),
        approval_bound_entries=sum(
            1 for entry in entries if entry.requires_explicit_approval
        ),
        read_only_fallback_entries=sum(
            1 for entry in entries if entry.read_only_fallback
        ),
        entries=entries,
    )

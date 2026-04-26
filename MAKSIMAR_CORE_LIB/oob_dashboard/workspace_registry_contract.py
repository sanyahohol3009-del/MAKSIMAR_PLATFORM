from __future__ import annotations

from MAKSIMAR_CORE_LIB.oob_dashboard.panel_view_display_chain_contract import (
    build_panel_view_display_chain_contract,
)
from MAKSIMAR_CORE_LIB.oob_dashboard.workspace_registry_models import (
    WorkspaceRegistryContract,
    WorkspaceRegistryEntry,
)


def build_workspace_registry_contract() -> WorkspaceRegistryContract:
    """Build the canonical workspace registry contract."""
    chain_contract = build_panel_view_display_chain_contract()

    foundation_panels = tuple(
        entry.panel_id
        for entry in chain_contract.entries
        if entry.display_target_id in {
            "display_foundation_primary",
            "display_foundation_secondary",
        }
    )
    interaction_panels = tuple(
        entry.panel_id
        for entry in chain_contract.entries
        if entry.display_target_id == "display_operator_interaction"
    )

    entries = (
        WorkspaceRegistryEntry(
            workspace_id="workspace_foundation_monitoring",
            workspace_role="foundation_monitoring",
            primary_display_target_id="display_foundation_primary",
            included_panel_ids=foundation_panels,
            description="Canonical workspace for foundation monitoring panels.",
        ),
        WorkspaceRegistryEntry(
            workspace_id="workspace_operator_interaction",
            workspace_role="operator_interaction",
            primary_display_target_id="display_operator_interaction",
            included_panel_ids=interaction_panels,
            description="Canonical workspace for operator interaction panels.",
        ),
    )

    return WorkspaceRegistryContract(entries=entries)

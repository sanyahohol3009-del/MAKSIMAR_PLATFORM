from __future__ import annotations

from MAKSIMAR_CORE_LIB.oob_dashboard.display_target_vocabulary_contract import (
    build_display_target_vocabulary_contract,
)
from MAKSIMAR_CORE_LIB.oob_dashboard.panel_binding_contract import (
    build_panel_binding_contract,
)
from MAKSIMAR_CORE_LIB.oob_dashboard.panel_view_display_chain_models import (
    PanelViewDisplayChainContract,
    PanelViewDisplayChainEntry,
)
from MAKSIMAR_CORE_LIB.oob_dashboard.view_targeting_contract import (
    build_view_targeting_contract,
)


def build_panel_view_display_chain_contract() -> PanelViewDisplayChainContract:
    """Build the canonical panel → view → display chain contract."""
    panel_binding_contract = build_panel_binding_contract()
    view_targeting_contract = build_view_targeting_contract()
    display_vocabulary_contract = build_display_target_vocabulary_contract()

    panel_binding_map = {entry.panel_id: entry for entry in panel_binding_contract.entries}
    view_targeting_map = {entry.panel_id: entry for entry in view_targeting_contract.entries}
    display_map = {
        entry.display_target_id: entry for entry in display_vocabulary_contract.entries
    }

    entries = tuple(
        PanelViewDisplayChainEntry(
            panel_id=panel_id,
            view_id=view_targeting_map[panel_id].view_id,
            display_target_id=panel_binding_map[panel_id].display_target_id,
            display_role=display_map[panel_binding_map[panel_id].display_target_id].display_role,
            display_zone=display_map[panel_binding_map[panel_id].display_target_id].display_zone,
            is_default_chain=panel_binding_map[panel_id].is_default_target,
            description=f"Canonical panel → view → display chain for {panel_id}.",
        )
        for panel_id in panel_binding_map
    )

    return PanelViewDisplayChainContract(entries=entries)

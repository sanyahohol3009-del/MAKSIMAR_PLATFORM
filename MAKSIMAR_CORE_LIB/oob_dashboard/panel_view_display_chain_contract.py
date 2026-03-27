from __future__ import annotations

from dataclasses import dataclass

from MAKSIMAR_CORE_LIB.oob_dashboard.display_target_vocabulary_contract import (
    build_display_target_vocabulary_contract,
)
from MAKSIMAR_CORE_LIB.oob_dashboard.panel_binding_contract import (
    build_panel_binding_contract,
)
from MAKSIMAR_CORE_LIB.oob_dashboard.view_targeting_contract import (
    build_view_targeting_contract,
)


@dataclass(frozen=True, slots=True)
class PanelViewDisplayChainEntry:
    """Canonical chain entry connecting panel, view, and display target."""

    panel_id: str
    view_id: str
    display_target_id: str
    display_role: str
    display_zone: str
    is_default_chain: bool
    description: str


@dataclass(frozen=True, slots=True)
class PanelViewDisplayChainContract:
    """Canonical panel → view → display chain contract."""

    total_entries: int
    primary_operator_chains: int
    diagnostics_chains: int
    expansion_chains: int
    default_chains: int
    entries: tuple[PanelViewDisplayChainEntry, ...]


def build_panel_view_display_chain_contract() -> PanelViewDisplayChainContract:
    """Build canonical panel → view → display chain contract."""
    panel_binding_contract = build_panel_binding_contract()
    view_targeting_contract = build_view_targeting_contract()
    display_contract = build_display_target_vocabulary_contract()

    panel_binding_map = {entry.panel_id: entry for entry in panel_binding_contract.entries}
    view_targeting_map = {entry.panel_id: entry for entry in view_targeting_contract.entries}
    display_map = {entry.display_target_id: entry for entry in display_contract.entries}

    entries = tuple(
        PanelViewDisplayChainEntry(
            panel_id=panel_id,
            view_id=view_targeting_map[panel_id].view_id,
            display_target_id=panel_binding_map[panel_id].display_target_id,
            display_role=display_map[panel_binding_map[panel_id].display_target_id].display_role,
            display_zone=display_map[panel_binding_map[panel_id].display_target_id].display_zone,
            is_default_chain=panel_binding_map[panel_id].is_default_target,
            description=(
                f"Canonical panel → view → display chain for {panel_id}."
            ),
        )
        for panel_id in panel_binding_map
    )

    return PanelViewDisplayChainContract(
        total_entries=len(entries),
        primary_operator_chains=sum(
            1 for entry in entries if entry.display_target_id == "display_primary_operator"
        ),
        diagnostics_chains=sum(
            1 for entry in entries if entry.display_target_id == "display_secondary_diagnostics"
        ),
        expansion_chains=sum(
            1 for entry in entries if entry.display_target_id == "display_tertiary_expansion"
        ),
        default_chains=sum(1 for entry in entries if entry.is_default_chain),
        entries=entries,
    )

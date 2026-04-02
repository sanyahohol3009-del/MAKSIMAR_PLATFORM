from __future__ import annotations

from dataclasses import dataclass
from typing import Literal

from MAKSIMAR_CORE_LIB.oob_dashboard.panel_metadata_contract import (
    build_panel_metadata_contract,
)
from MAKSIMAR_CORE_LIB.oob_dashboard.panel_view_display_chain_contract import (
    build_panel_view_display_chain_contract,
)
from MAKSIMAR_CORE_LIB.oob_dashboard.visual_theme_contract import (
    build_visual_theme_contract,
)


VisualCardType = Literal[
    "status_core_card",
    "diagnostics_card",
    "topology_card",
    "navigation_card",
    "operator_card",
    "admin_card",
]

VisualDensityMode = Literal[
    "compact",
    "expanded",
    "focus",
]

InteractionClass = Literal[
    "read_only",
    "proposal_only",
    "interactive_controlled",
]

VisualPriority = Literal[
    "primary",
    "secondary",
    "supporting",
]


@dataclass(frozen=True, slots=True)
class PanelToVisualMappingEntry:
    """Canonical mapping from panel contract to visual renderer surface."""

    panel_id: str
    display_title: str
    visual_card_type: VisualCardType
    preferred_zone: str
    visual_priority: VisualPriority
    density_mode: VisualDensityMode
    icon_slot: str
    title_slot: str
    signal_overlay_participation: bool
    topology_overlay_participation: bool
    explainability_binding: bool
    interaction_class: InteractionClass
    theme_id: str
    description: str


@dataclass(frozen=True, slots=True)
class PanelToVisualMappingContract:
    """Canonical mapping contract from panels to visual renderer presentation."""

    contract_id: str
    total_entries: int
    signal_overlay_entries: int
    topology_overlay_entries: int
    explainability_entries: int
    read_only_entries: int
    proposal_only_entries: int
    interactive_controlled_entries: int
    entries: tuple[PanelToVisualMappingEntry, ...]


def _visual_card_type_for_panel(
    panel_id: str,
    panel_state_class: str,
) -> VisualCardType:
    """Resolve visual card type from canonical panel identity and state class."""
    if panel_id == "panel_navigation":
        return "navigation_card"
    if panel_state_class == "foundation":
        return "status_core_card"
    if panel_state_class == "diagnostics":
        return "diagnostics_card"
    if panel_state_class == "topology":
        return "topology_card"
    if panel_state_class == "operator":
        return "operator_card"
    if panel_state_class == "admin":
        return "admin_card"
    return "navigation_card"


def _priority_for_panel(
    panel_id: str,
    panel_state_class: str,
) -> VisualPriority:
    """Resolve visual priority from canonical panel identity and state class."""
    if panel_id == "panel_navigation":
        return "supporting"
    if panel_state_class in {"foundation", "operator"}:
        return "primary"
    if panel_state_class in {"diagnostics", "topology"}:
        return "secondary"
    return "supporting"


def _density_for_panel(
    panel_id: str,
    panel_state_class: str,
) -> VisualDensityMode:
    """Resolve default visual density from canonical panel identity and state class."""
    if panel_id == "panel_navigation":
        return "compact"
    if panel_state_class == "foundation":
        return "focus"
    if panel_state_class in {"diagnostics", "operator"}:
        return "expanded"
    return "compact"


def _interaction_class_for_read_mode(read_mode: str) -> InteractionClass:
    """Resolve interaction class from canonical read mode."""
    if read_mode == "read_only":
        return "read_only"
    if read_mode == "interactive_controlled":
        return "interactive_controlled"
    return "proposal_only"


def _icon_slot_for_panel(panel_id: str, panel_state_class: str) -> str:
    """Resolve icon slot for a panel."""
    if panel_id.startswith("panel_foundation_"):
        return "core_status_icon"
    if panel_state_class == "diagnostics":
        return "diagnostics_icon"
    if panel_state_class == "topology":
        return "topology_icon"
    if panel_state_class == "operator":
        return "operator_icon"
    if panel_state_class == "admin":
        return "admin_icon"
    return "navigation_icon"


def _zone_for_panel(panel_id: str, panel_state_class: str) -> str:
    """Resolve preferred visual zone for a panel."""
    if panel_id == "panel_navigation":
        return "left_navigation"
    if panel_state_class == "foundation":
        return "center_core"
    if panel_state_class == "operator":
        return "right_operator"
    if panel_state_class == "diagnostics":
        return "right_explainable"
    if panel_state_class == "topology":
        return "center_ring"
    return "bottom_status"


def build_panel_to_visual_mapping_contract() -> PanelToVisualMappingContract:
    """Build canonical panel to visual mapping contract."""
    panel_metadata_contract = build_panel_metadata_contract()
    panel_chain_contract = build_panel_view_display_chain_contract()
    visual_theme_contract = build_visual_theme_contract()

    theme_id = visual_theme_contract.entries[0].theme_id
    chain_panel_ids = {entry.panel_id for entry in panel_chain_contract.entries}

    entries = tuple(
        PanelToVisualMappingEntry(
            panel_id=metadata_entry.panel_id,
            display_title=metadata_entry.display_title,
            visual_card_type=_visual_card_type_for_panel(
                metadata_entry.panel_id,
                metadata_entry.panel_state_class,
            ),
            preferred_zone=_zone_for_panel(
                metadata_entry.panel_id,
                metadata_entry.panel_state_class,
            ),
            visual_priority=_priority_for_panel(
                metadata_entry.panel_id,
                metadata_entry.panel_state_class,
            ),
            density_mode=_density_for_panel(
                metadata_entry.panel_id,
                metadata_entry.panel_state_class,
            ),
            icon_slot=_icon_slot_for_panel(
                metadata_entry.panel_id,
                metadata_entry.panel_state_class,
            ),
            title_slot="panel_title_primary",
            signal_overlay_participation=metadata_entry.panel_id in chain_panel_ids,
            topology_overlay_participation=(
                metadata_entry.panel_state_class in {"foundation", "topology"}
            ),
            explainability_binding=(
                metadata_entry.panel_state_class
                in {"foundation", "diagnostics", "operator"}
            ),
            interaction_class=_interaction_class_for_read_mode(
                metadata_entry.read_mode
            ),
            theme_id=theme_id,
            description=(
                f"Canonical visual mapping entry for {metadata_entry.panel_id}."
            ),
        )
        for metadata_entry in panel_metadata_contract.entries
    )

    return PanelToVisualMappingContract(
        contract_id="panel_to_visual_mapping_contract_001",
        total_entries=len(entries),
        signal_overlay_entries=sum(
            1 for entry in entries if entry.signal_overlay_participation
        ),
        topology_overlay_entries=sum(
            1 for entry in entries if entry.topology_overlay_participation
        ),
        explainability_entries=sum(
            1 for entry in entries if entry.explainability_binding
        ),
        read_only_entries=sum(
            1 for entry in entries if entry.interaction_class == "read_only"
        ),
        proposal_only_entries=sum(
            1 for entry in entries if entry.interaction_class == "proposal_only"
        ),
        interactive_controlled_entries=sum(
            1
            for entry in entries
            if entry.interaction_class == "interactive_controlled"
        ),
        entries=entries,
    )

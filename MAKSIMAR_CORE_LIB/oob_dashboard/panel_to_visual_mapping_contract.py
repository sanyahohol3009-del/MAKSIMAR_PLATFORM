from __future__ import annotations

from dataclasses import dataclass
from typing import Tuple


@dataclass(frozen=True)
class PanelToVisualMappingEntry:
    """Canonical backward-compatible panel-to-visual mapping entry."""

    panel_id: str
    display_title: str
    visual_card_type: str
    preferred_zone: str
    visual_priority: str
    density_mode: str
    icon_slot: str
    theme_id: str
    title_slot: str
    signal_overlay_enabled: bool
    signal_overlay_participation: bool
    topology_overlay_enabled: bool
    topology_overlay_participation: bool
    explainability_enabled: bool
    explainability_binding: bool
    interaction_class: str
    read_only: bool
    operator_visible: bool
    description: str


@dataclass(frozen=True)
class PanelToVisualMappingContract:
    """Canonical backward-compatible panel-to-visual mapping contract."""

    contract_id: str
    total_entries: int
    signal_overlay_entries: int
    topology_overlay_entries: int
    explainability_entries: int
    read_only_entries: int
    entries: Tuple[PanelToVisualMappingEntry, ...]
    operator_visible: bool
    description: str


def build_panel_to_visual_mapping_contract() -> PanelToVisualMappingContract:
    """Build canonical backward-compatible panel-to-visual mapping contract."""
    entries = (
        PanelToVisualMappingEntry(
            panel_id="panel_foundation_runtime_status_001",
            display_title="Runtime Core",
            visual_card_type="status_core_card",
            preferred_zone="center_core",
            visual_priority="primary",
            density_mode="focus",
            icon_slot="core_status_icon",
            theme_id="visual_theme_operator_hud_001",
            title_slot="panel_title_primary",
            signal_overlay_enabled=True,
            signal_overlay_participation=True,
            topology_overlay_enabled=True,
            topology_overlay_participation=True,
            explainability_enabled=True,
            explainability_binding=True,
            interaction_class="read_only",
            read_only=True,
            operator_visible=True,
            description="Canonical runtime foundation visual mapping entry.",
        ),
        PanelToVisualMappingEntry(
            panel_id="panel_navigation",
            display_title="Navigation",
            visual_card_type="navigation_card",
            preferred_zone="left_navigation",
            visual_priority="supporting",
            density_mode="compact",
            icon_slot="navigation_icon",
            theme_id="visual_theme_operator_hud_001",
            title_slot="panel_title_primary",
            signal_overlay_enabled=True,
            signal_overlay_participation=True,
            topology_overlay_enabled=False,
            topology_overlay_participation=False,
            explainability_enabled=False,
            explainability_binding=False,
            interaction_class="read_only",
            read_only=True,
            operator_visible=True,
            description="Canonical navigation visual mapping entry.",
        ),
        PanelToVisualMappingEntry(
            panel_id="panel_consistency",
            display_title="Consistency",
            visual_card_type="summary_card",
            preferred_zone="right_diagnostics",
            visual_priority="supporting",
            density_mode="compact",
            icon_slot="consistency_icon",
            theme_id="visual_theme_operator_hud_001",
            title_slot="panel_title_primary",
            signal_overlay_enabled=False,
            signal_overlay_participation=False,
            topology_overlay_enabled=False,
            topology_overlay_participation=False,
            explainability_enabled=False,
            explainability_binding=False,
            interaction_class="read_only",
            read_only=True,
            operator_visible=True,
            description="Canonical consistency visual mapping entry.",
        ),
    )

    return PanelToVisualMappingContract(
        contract_id="panel_to_visual_mapping_contract_001",
        total_entries=len(entries),
        signal_overlay_entries=sum(1 for entry in entries if entry.signal_overlay_enabled),
        topology_overlay_entries=sum(1 for entry in entries if entry.topology_overlay_enabled),
        explainability_entries=sum(1 for entry in entries if entry.explainability_enabled),
        read_only_entries=sum(1 for entry in entries if entry.read_only),
        entries=entries,
        operator_visible=True,
        description="Canonical backward-compatible panel-to-visual mapping contract.",
    )

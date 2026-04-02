from __future__ import annotations

from dataclasses import dataclass
from typing import Literal

from MAKSIMAR_CORE_LIB.oob_dashboard.panel_to_visual_mapping_contract import (
    build_panel_to_visual_mapping_contract,
)
from MAKSIMAR_CORE_LIB.oob_dashboard.visual_theme_hardening_contract import (
    build_visual_theme_hardening_contract,
)


HierarchyHardeningMode = Literal[
    "phase_1_panel_hierarchy_hardening",
]

HierarchyEmphasisProfile = Literal[
    "operator_hud_priority_stack",
]

FrameConsistencyProfile = Literal[
    "premium_hud_frame_consistency",
]


@dataclass(frozen=True, slots=True)
class VisualPanelHierarchyHardeningEntry:
    """Canonical Phase 1 panel hierarchy hardening entry."""

    hardening_id: str
    theme_hardening_id: str
    hierarchy_hardening_mode: HierarchyHardeningMode
    emphasis_profile: HierarchyEmphasisProfile
    frame_consistency_profile: FrameConsistencyProfile
    total_panels: int
    primary_panels: int
    secondary_panels: int
    supporting_panels: int
    stronger_foundation_hierarchy: bool
    stronger_operator_hierarchy: bool
    stronger_explainability_hierarchy: bool
    stronger_navigation_hierarchy: bool
    read_only: bool
    description: str


@dataclass(frozen=True, slots=True)
class VisualPanelHierarchyHardeningContract:
    """Canonical Phase 1 panel hierarchy hardening contract."""

    contract_id: str
    total_entries: int
    read_only_entries: int
    stronger_foundation_entries: int
    stronger_operator_entries: int
    entries: tuple[VisualPanelHierarchyHardeningEntry, ...]


def build_visual_panel_hierarchy_hardening_contract(
    ) -> VisualPanelHierarchyHardeningContract:
    """Build canonical Phase 1 panel hierarchy hardening contract."""
    mapping_contract = build_panel_to_visual_mapping_contract()
    theme_hardening_contract = build_visual_theme_hardening_contract()
    theme_hardening_entry = theme_hardening_contract.entries[0]

    primary_panels = sum(
        1 for entry in mapping_contract.entries if entry.visual_priority == "primary"
    )
    secondary_panels = sum(
        1 for entry in mapping_contract.entries if entry.visual_priority == "secondary"
    )
    supporting_panels = sum(
        1 for entry in mapping_contract.entries if entry.visual_priority == "supporting"
    )

    entries = (
        VisualPanelHierarchyHardeningEntry(
            hardening_id="visual_panel_hierarchy_hardening_001",
            theme_hardening_id=theme_hardening_entry.hardening_id,
            hierarchy_hardening_mode="phase_1_panel_hierarchy_hardening",
            emphasis_profile="operator_hud_priority_stack",
            frame_consistency_profile="premium_hud_frame_consistency",
            total_panels=mapping_contract.total_entries,
            primary_panels=primary_panels,
            secondary_panels=secondary_panels,
            supporting_panels=supporting_panels,
            stronger_foundation_hierarchy=True,
            stronger_operator_hierarchy=True,
            stronger_explainability_hierarchy=True,
            stronger_navigation_hierarchy=True,
            read_only=True,
            description=(
                "Canonical Phase 1 panel hierarchy hardening entry for "
                "truth-preserving HUD refinement."
            ),
        ),
    )

    return VisualPanelHierarchyHardeningContract(
        contract_id="visual_panel_hierarchy_hardening_contract_001",
        total_entries=len(entries),
        read_only_entries=sum(1 for entry in entries if entry.read_only),
        stronger_foundation_entries=sum(
            1 for entry in entries if entry.stronger_foundation_hierarchy
        ),
        stronger_operator_entries=sum(
            1 for entry in entries if entry.stronger_operator_hierarchy
        ),
        entries=entries,
    )

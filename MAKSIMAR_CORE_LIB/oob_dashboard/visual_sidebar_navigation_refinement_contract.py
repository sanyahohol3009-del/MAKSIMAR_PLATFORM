from __future__ import annotations

from dataclasses import dataclass
from typing import Literal

from MAKSIMAR_CORE_LIB.oob_dashboard.visual_center_core_refinement_contract import (
    build_visual_center_core_refinement_contract,
)
from MAKSIMAR_CORE_LIB.oob_dashboard.visual_explainability_sidebar_contract import (
    build_visual_explainability_sidebar_contract,
)
from MAKSIMAR_CORE_LIB.oob_dashboard.visual_panel_hierarchy_hardening_contract import (
    build_visual_panel_hierarchy_hardening_contract,
)


SidebarNavigationRefinementMode = Literal[
    "phase_1_sidebar_navigation_refinement",
]

NavigationClarityProfile = Literal[
    "strong_left_navigation_readability",
]

SidebarClarityProfile = Literal[
    "strong_right_explainability_readability",
]

OperatorTrustProfile = Literal[
    "clear_operator_guidance",
]


@dataclass(frozen=True, slots=True)
class VisualSidebarNavigationRefinementEntry:
    """Canonical Phase 1 sidebar/navigation refinement entry."""

    refinement_id: str
    center_core_refinement_id: str
    hierarchy_hardening_id: str
    refinement_mode: SidebarNavigationRefinementMode
    navigation_clarity_profile: NavigationClarityProfile
    sidebar_clarity_profile: SidebarClarityProfile
    operator_trust_profile: OperatorTrustProfile
    explainability_entries: int
    stronger_left_navigation_hierarchy: bool
    stronger_right_sidebar_hierarchy: bool
    stronger_active_state_readability: bool
    stronger_operator_guidance_clarity: bool
    read_only: bool
    description: str


@dataclass(frozen=True, slots=True)
class VisualSidebarNavigationRefinementContract:
    """Canonical Phase 1 sidebar/navigation refinement contract."""

    contract_id: str
    total_entries: int
    read_only_entries: int
    stronger_navigation_entries: int
    stronger_sidebar_entries: int
    entries: tuple[VisualSidebarNavigationRefinementEntry, ...]


def build_visual_sidebar_navigation_refinement_contract(
    ) -> VisualSidebarNavigationRefinementContract:
    """Build canonical Phase 1 sidebar/navigation refinement contract."""
    center_core_contract = build_visual_center_core_refinement_contract()
    hierarchy_contract = build_visual_panel_hierarchy_hardening_contract()
    explainability_contract = build_visual_explainability_sidebar_contract()

    center_core_entry = center_core_contract.entries[0]
    hierarchy_entry = hierarchy_contract.entries[0]

    entries = (
        VisualSidebarNavigationRefinementEntry(
            refinement_id="visual_sidebar_navigation_refinement_001",
            center_core_refinement_id=center_core_entry.refinement_id,
            hierarchy_hardening_id=hierarchy_entry.hardening_id,
            refinement_mode="phase_1_sidebar_navigation_refinement",
            navigation_clarity_profile="strong_left_navigation_readability",
            sidebar_clarity_profile="strong_right_explainability_readability",
            operator_trust_profile="clear_operator_guidance",
            explainability_entries=explainability_contract.total_entries,
            stronger_left_navigation_hierarchy=True,
            stronger_right_sidebar_hierarchy=True,
            stronger_active_state_readability=True,
            stronger_operator_guidance_clarity=True,
            read_only=True,
            description=(
                "Canonical Phase 1 sidebar/navigation refinement entry for "
                "truth-preserving operator HUD polish."
            ),
        ),
    )

    return VisualSidebarNavigationRefinementContract(
        contract_id="visual_sidebar_navigation_refinement_contract_001",
        total_entries=len(entries),
        read_only_entries=sum(1 for entry in entries if entry.read_only),
        stronger_navigation_entries=sum(
            1 for entry in entries if entry.stronger_left_navigation_hierarchy
        ),
        stronger_sidebar_entries=sum(
            1 for entry in entries if entry.stronger_right_sidebar_hierarchy
        ),
        entries=entries,
    )

from __future__ import annotations

from dataclasses import dataclass
from typing import Literal

from MAKSIMAR_CORE_LIB.oob_dashboard.visual_theme_hardening_contract import (
    build_visual_theme_hardening_contract,
)
from MAKSIMAR_CORE_LIB.oob_dashboard.visual_panel_hierarchy_hardening_contract import (
    build_visual_panel_hierarchy_hardening_contract,
)
from MAKSIMAR_CORE_LIB.oob_dashboard.visual_center_core_refinement_contract import (
    build_visual_center_core_refinement_contract,
)
from MAKSIMAR_CORE_LIB.oob_dashboard.visual_sidebar_navigation_refinement_contract import (
    build_visual_sidebar_navigation_refinement_contract,
)
from MAKSIMAR_CORE_LIB.oob_dashboard.visual_status_ticker_refinement_contract import (
    build_visual_status_ticker_refinement_contract,
)


Phase1ReadinessMode = Literal[
    "phase_1_visual_polish_readiness",
]

Phase1Status = Literal[
    "ready_for_preview_render_polish",
]


@dataclass(frozen=True, slots=True)
class VisualPhase1ReadinessEntry:
    """Canonical Phase 1 visual polish readiness entry."""

    readiness_id: str
    readiness_mode: Phase1ReadinessMode
    readiness_status: Phase1Status
    theme_hardening_id: str
    panel_hierarchy_hardening_id: str
    center_core_refinement_id: str
    sidebar_navigation_refinement_id: str
    status_ticker_refinement_id: str
    theme_hardening_complete: bool
    panel_hierarchy_complete: bool
    center_core_complete: bool
    sidebar_navigation_complete: bool
    status_ticker_complete: bool
    read_only: bool
    description: str


@dataclass(frozen=True, slots=True)
class VisualPhase1ReadinessContract:
    """Canonical Phase 1 visual polish readiness contract."""

    contract_id: str
    total_entries: int
    ready_entries: int
    read_only_entries: int
    entries: tuple[VisualPhase1ReadinessEntry, ...]


def build_visual_phase_1_readiness_contract() -> VisualPhase1ReadinessContract:
    """Build canonical Phase 1 visual polish readiness contract."""
    theme_contract = build_visual_theme_hardening_contract()
    panel_hierarchy_contract = build_visual_panel_hierarchy_hardening_contract()
    center_core_contract = build_visual_center_core_refinement_contract()
    sidebar_navigation_contract = build_visual_sidebar_navigation_refinement_contract()
    status_ticker_contract = build_visual_status_ticker_refinement_contract()

    theme_entry = theme_contract.entries[0]
    panel_hierarchy_entry = panel_hierarchy_contract.entries[0]
    center_core_entry = center_core_contract.entries[0]
    sidebar_navigation_entry = sidebar_navigation_contract.entries[0]
    status_ticker_entry = status_ticker_contract.entries[0]

    entries = (
        VisualPhase1ReadinessEntry(
            readiness_id="visual_phase_1_readiness_001",
            readiness_mode="phase_1_visual_polish_readiness",
            readiness_status="ready_for_preview_render_polish",
            theme_hardening_id=theme_entry.hardening_id,
            panel_hierarchy_hardening_id=panel_hierarchy_entry.hardening_id,
            center_core_refinement_id=center_core_entry.refinement_id,
            sidebar_navigation_refinement_id=sidebar_navigation_entry.refinement_id,
            status_ticker_refinement_id=status_ticker_entry.refinement_id,
            theme_hardening_complete=True,
            panel_hierarchy_complete=True,
            center_core_complete=True,
            sidebar_navigation_complete=True,
            status_ticker_complete=True,
            read_only=True,
            description=(
                "Canonical Phase 1 readiness entry after completion of the "
                "allowed truth-preserving visual polish passes."
            ),
        ),
    )

    return VisualPhase1ReadinessContract(
        contract_id="visual_phase_1_readiness_contract_001",
        total_entries=len(entries),
        ready_entries=sum(
            1
            for entry in entries
            if entry.readiness_status == "ready_for_preview_render_polish"
        ),
        read_only_entries=sum(1 for entry in entries if entry.read_only),
        entries=entries,
    )

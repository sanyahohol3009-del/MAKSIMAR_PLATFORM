from __future__ import annotations

from dataclasses import dataclass
from typing import Literal

from MAKSIMAR_CORE_LIB.oob_dashboard.visual_hud_preview_state_contract import (
    build_visual_hud_preview_state_contract,
)
from MAKSIMAR_CORE_LIB.oob_dashboard.visual_phase_1_readiness_contract import (
    build_visual_phase_1_readiness_contract,
)


PreviewRenderPolishMode = Literal[
    "preview_render_polish_readiness",
]

PreviewRenderPolishStatus = Literal[
    "ready_for_preview_render_polish",
]


@dataclass(frozen=True, slots=True)
class VisualPreviewRenderPolishReadinessEntry:
    """Canonical readiness entry for preview/render polish after Phase 1."""

    readiness_id: str
    phase_1_readiness_id: str
    preview_state_id: str
    readiness_mode: PreviewRenderPolishMode
    readiness_status: PreviewRenderPolishStatus
    theme_hardening_ready: bool
    panel_hierarchy_ready: bool
    center_core_ready: bool
    sidebar_navigation_ready: bool
    status_ticker_ready: bool
    preview_state_ready: bool
    read_only: bool
    description: str


@dataclass(frozen=True, slots=True)
class VisualPreviewRenderPolishReadinessContract:
    """Canonical contract for preview/render polish readiness."""

    contract_id: str
    total_entries: int
    ready_entries: int
    read_only_entries: int
    entries: tuple[VisualPreviewRenderPolishReadinessEntry, ...]


def build_visual_preview_render_polish_readiness_contract(
    ) -> VisualPreviewRenderPolishReadinessContract:
    """Build canonical preview/render polish readiness contract."""
    phase_1_contract = build_visual_phase_1_readiness_contract()
    preview_state_contract = build_visual_hud_preview_state_contract()

    phase_1_entry = phase_1_contract.entries[0]
    preview_state_entry = preview_state_contract.entries[0]

    entries = (
        VisualPreviewRenderPolishReadinessEntry(
            readiness_id="visual_preview_render_polish_readiness_001",
            phase_1_readiness_id=phase_1_entry.readiness_id,
            preview_state_id=preview_state_entry.preview_state_id,
            readiness_mode="preview_render_polish_readiness",
            readiness_status="ready_for_preview_render_polish",
            theme_hardening_ready=phase_1_entry.theme_hardening_complete,
            panel_hierarchy_ready=phase_1_entry.panel_hierarchy_complete,
            center_core_ready=phase_1_entry.center_core_complete,
            sidebar_navigation_ready=phase_1_entry.sidebar_navigation_complete,
            status_ticker_ready=phase_1_entry.status_ticker_complete,
            preview_state_ready=(
                preview_state_entry.preview_state_status == "stable"
            ),
            read_only=True,
            description=(
                "Canonical readiness entry for preview/render polish after "
                "completion of the allowed Phase 1 visual refinement passes."
            ),
        ),
    )

    return VisualPreviewRenderPolishReadinessContract(
        contract_id="visual_preview_render_polish_readiness_contract_001",
        total_entries=len(entries),
        ready_entries=sum(
            1
            for entry in entries
            if entry.readiness_status == "ready_for_preview_render_polish"
        ),
        read_only_entries=sum(1 for entry in entries if entry.read_only),
        entries=entries,
    )

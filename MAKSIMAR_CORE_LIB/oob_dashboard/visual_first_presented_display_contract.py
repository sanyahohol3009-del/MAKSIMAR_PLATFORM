from __future__ import annotations

from dataclasses import dataclass
from typing import Literal

from MAKSIMAR_CORE_LIB.oob_dashboard.visual_first_watchable_display_contract import (
    build_visual_first_watchable_display_contract,
)


PresentedDisplayMode = Literal[
    "first_presented_display",
]

PresentedDisplayStatus = Literal[
    "presented_display_ready",
]


@dataclass(frozen=True, slots=True)
class VisualFirstPresentedDisplayEntry:
    """Canonical first presented display entry."""

    presented_display_id: str
    watchable_display_id: str
    presented_display_mode: PresentedDisplayMode
    presented_display_status: PresentedDisplayStatus
    renderer_surface_id: str
    theme_id: str
    screen_id: str
    preview_artifact_id: str
    watchable_display_ready: bool
    presented_display_ready: bool
    truth_bound_presented_display: bool
    read_only: bool
    description: str


@dataclass(frozen=True, slots=True)
class VisualFirstPresentedDisplayContract:
    """Canonical first presented display contract."""

    contract_id: str
    total_entries: int
    ready_entries: int
    read_only_entries: int
    entries: tuple[VisualFirstPresentedDisplayEntry, ...]


def build_visual_first_presented_display_contract() -> VisualFirstPresentedDisplayContract:
    """Build canonical first presented display contract."""
    watchable_display_contract = build_visual_first_watchable_display_contract()
    watchable_display_entry = watchable_display_contract.entries[0]

    entries = (
        VisualFirstPresentedDisplayEntry(
            presented_display_id="visual_first_presented_display_001",
            watchable_display_id=watchable_display_entry.watchable_display_id,
            presented_display_mode="first_presented_display",
            presented_display_status="presented_display_ready",
            renderer_surface_id=watchable_display_entry.renderer_surface_id,
            theme_id=watchable_display_entry.theme_id,
            screen_id=watchable_display_entry.screen_id,
            preview_artifact_id=watchable_display_entry.preview_artifact_id,
            watchable_display_ready=watchable_display_entry.watchable_display_ready,
            presented_display_ready=True,
            truth_bound_presented_display=True,
            read_only=True,
            description=(
                "Canonical first presented display entry after assembly of "
                "the first truth-preserving watchable display."
            ),
        ),
    )

    return VisualFirstPresentedDisplayContract(
        contract_id="visual_first_presented_display_contract_001",
        total_entries=len(entries),
        ready_entries=sum(
            1
            for entry in entries
            if entry.presented_display_status == "presented_display_ready"
        ),
        read_only_entries=sum(1 for entry in entries if entry.read_only),
        entries=entries,
    )

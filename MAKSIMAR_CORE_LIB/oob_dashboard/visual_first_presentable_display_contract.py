from __future__ import annotations

from dataclasses import dataclass
from typing import Literal

from MAKSIMAR_CORE_LIB.oob_dashboard.visual_first_displayable_view_contract import (
    build_visual_first_displayable_view_contract,
)


PresentableDisplayMode = Literal[
    "first_presentable_display",
]

PresentableDisplayStatus = Literal[
    "presentable_display_ready",
]


@dataclass(frozen=True, slots=True)
class VisualFirstPresentableDisplayEntry:
    """Canonical first presentable display entry."""

    display_id: str
    displayable_view_id: str
    display_mode: PresentableDisplayMode
    display_status: PresentableDisplayStatus
    renderer_surface_id: str
    theme_id: str
    screen_id: str
    preview_artifact_id: str
    displayable_ready: bool
    presentable_display_ready: bool
    truth_bound_display: bool
    read_only: bool
    description: str


@dataclass(frozen=True, slots=True)
class VisualFirstPresentableDisplayContract:
    """Canonical first presentable display contract."""

    contract_id: str
    total_entries: int
    ready_entries: int
    read_only_entries: int
    entries: tuple[VisualFirstPresentableDisplayEntry, ...]


def build_visual_first_presentable_display_contract(
) -> VisualFirstPresentableDisplayContract:
    """Build canonical first presentable display contract."""
    displayable_view_contract = build_visual_first_displayable_view_contract()
    displayable_view_entry = displayable_view_contract.entries[0]

    entries = (
        VisualFirstPresentableDisplayEntry(
            display_id="visual_first_presentable_display_001",
            displayable_view_id=displayable_view_entry.displayable_view_id,
            display_mode="first_presentable_display",
            display_status="presentable_display_ready",
            renderer_surface_id=displayable_view_entry.renderer_surface_id,
            theme_id=displayable_view_entry.theme_id,
            screen_id=displayable_view_entry.screen_id,
            preview_artifact_id=displayable_view_entry.preview_artifact_id,
            displayable_ready=displayable_view_entry.displayable_ready,
            presentable_display_ready=True,
            truth_bound_display=True,
            read_only=True,
            description=(
                "Canonical first presentable display entry after assembly of "
                "the first truth-preserving displayable view."
            ),
        ),
    )

    return VisualFirstPresentableDisplayContract(
        contract_id="visual_first_presentable_display_contract_001",
        total_entries=len(entries),
        ready_entries=sum(
            1
            for entry in entries
            if entry.display_status == "presentable_display_ready"
        ),
        read_only_entries=sum(1 for entry in entries if entry.read_only),
        entries=entries,
    )

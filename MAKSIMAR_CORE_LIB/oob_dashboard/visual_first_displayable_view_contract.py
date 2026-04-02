from __future__ import annotations

from dataclasses import dataclass
from typing import Literal

from MAKSIMAR_CORE_LIB.oob_dashboard.visual_first_observable_view_contract import (
    build_visual_first_observable_view_contract,
)


DisplayableViewMode = Literal[
    "first_displayable_view",
]

DisplayableViewStatus = Literal[
    "displayable_view_ready",
]


@dataclass(frozen=True, slots=True)
class VisualFirstDisplayableViewEntry:
    """Canonical first displayable view entry."""

    displayable_view_id: str
    observable_view_id: str
    displayable_view_mode: DisplayableViewMode
    displayable_view_status: DisplayableViewStatus
    renderer_surface_id: str
    theme_id: str
    screen_id: str
    preview_artifact_id: str
    observable_ready: bool
    displayable_ready: bool
    truth_bound_displayable_view: bool
    read_only: bool
    description: str


@dataclass(frozen=True, slots=True)
class VisualFirstDisplayableViewContract:
    """Canonical first displayable view contract."""

    contract_id: str
    total_entries: int
    ready_entries: int
    read_only_entries: int
    entries: tuple[VisualFirstDisplayableViewEntry, ...]


def build_visual_first_displayable_view_contract(
) -> VisualFirstDisplayableViewContract:
    """Build canonical first displayable view contract."""
    observable_view_contract = build_visual_first_observable_view_contract()
    observable_view_entry = observable_view_contract.entries[0]

    entries = (
        VisualFirstDisplayableViewEntry(
            displayable_view_id="visual_first_displayable_view_001",
            observable_view_id=observable_view_entry.observable_view_id,
            displayable_view_mode="first_displayable_view",
            displayable_view_status="displayable_view_ready",
            renderer_surface_id=observable_view_entry.renderer_surface_id,
            theme_id=observable_view_entry.theme_id,
            screen_id=observable_view_entry.screen_id,
            preview_artifact_id=observable_view_entry.preview_artifact_id,
            observable_ready=observable_view_entry.observable_ready,
            displayable_ready=True,
            truth_bound_displayable_view=True,
            read_only=True,
            description=(
                "Canonical first displayable view entry after assembly of the "
                "first truth-preserving observable view."
            ),
        ),
    )

    return VisualFirstDisplayableViewContract(
        contract_id="visual_first_displayable_view_contract_001",
        total_entries=len(entries),
        ready_entries=sum(
            1
            for entry in entries
            if entry.displayable_view_status == "displayable_view_ready"
        ),
        read_only_entries=sum(1 for entry in entries if entry.read_only),
        entries=entries,
    )

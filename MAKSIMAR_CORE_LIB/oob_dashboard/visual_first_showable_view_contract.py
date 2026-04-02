from __future__ import annotations

from dataclasses import dataclass
from typing import Literal

from MAKSIMAR_CORE_LIB.oob_dashboard.visual_first_view_layer_contract import (
    build_visual_first_view_layer_contract,
)


ShowableViewMode = Literal[
    "first_showable_view",
]

ShowableViewStatus = Literal[
    "showable_view_ready",
]


@dataclass(frozen=True, slots=True)
class VisualFirstShowableViewEntry:
    """Canonical first showable view entry."""

    showable_view_id: str
    view_layer_id: str
    showable_view_mode: ShowableViewMode
    showable_view_status: ShowableViewStatus
    renderer_surface_id: str
    theme_id: str
    screen_id: str
    preview_artifact_id: str
    view_facing_ready: bool
    showable_ready: bool
    truth_bound_showable_view: bool
    read_only: bool
    description: str


@dataclass(frozen=True, slots=True)
class VisualFirstShowableViewContract:
    """Canonical first showable view contract."""

    contract_id: str
    total_entries: int
    ready_entries: int
    read_only_entries: int
    entries: tuple[VisualFirstShowableViewEntry, ...]


def build_visual_first_showable_view_contract() -> VisualFirstShowableViewContract:
    """Build canonical first showable view contract."""
    view_layer_contract = build_visual_first_view_layer_contract()
    view_layer_entry = view_layer_contract.entries[0]

    entries = (
        VisualFirstShowableViewEntry(
            showable_view_id="visual_first_showable_view_001",
            view_layer_id=view_layer_entry.view_layer_id,
            showable_view_mode="first_showable_view",
            showable_view_status="showable_view_ready",
            renderer_surface_id=view_layer_entry.renderer_surface_id,
            theme_id=view_layer_entry.theme_id,
            screen_id=view_layer_entry.screen_id,
            preview_artifact_id=view_layer_entry.preview_artifact_id,
            view_facing_ready=view_layer_entry.view_facing_ready,
            showable_ready=True,
            truth_bound_showable_view=True,
            read_only=True,
            description=(
                "Canonical first showable view entry after assembly of the "
                "first truth-preserving visual view layer."
            ),
        ),
    )

    return VisualFirstShowableViewContract(
        contract_id="visual_first_showable_view_contract_001",
        total_entries=len(entries),
        ready_entries=sum(
            1
            for entry in entries
            if entry.showable_view_status == "showable_view_ready"
        ),
        read_only_entries=sum(1 for entry in entries if entry.read_only),
        entries=entries,
    )

from __future__ import annotations

from dataclasses import dataclass
from typing import Literal

from MAKSIMAR_CORE_LIB.oob_dashboard.visual_first_screen_view_delivery_contract import (
    build_visual_first_screen_view_delivery_contract,
)


ScreenViewReadyMode = Literal[
    "first_screen_view_ready",
]

ScreenViewReadyStatus = Literal[
    "first_screen_view_ready_state",
]


@dataclass(frozen=True, slots=True)
class VisualFirstScreenViewReadyEntry:
    """Canonical first screen-view ready entry."""

    screen_view_ready_id: str
    screen_view_delivery_id: str
    screen_view_ready_mode: ScreenViewReadyMode
    screen_view_ready_status: ScreenViewReadyStatus
    renderer_surface_id: str
    theme_id: str
    screen_id: str
    preview_artifact_id: str
    screen_view_delivery_ready: bool
    screen_view_ready: bool
    truth_bound_screen_view_ready: bool
    read_only: bool
    description: str


@dataclass(frozen=True, slots=True)
class VisualFirstScreenViewReadyContract:
    """Canonical first screen-view ready contract."""

    contract_id: str
    total_entries: int
    ready_entries: int
    read_only_entries: int
    entries: tuple[VisualFirstScreenViewReadyEntry, ...]


def build_visual_first_screen_view_ready_contract(
) -> VisualFirstScreenViewReadyContract:
    """Build canonical first screen-view ready contract."""
    screen_view_delivery_contract = build_visual_first_screen_view_delivery_contract()
    screen_view_delivery_entry = screen_view_delivery_contract.entries[0]

    entries = (
        VisualFirstScreenViewReadyEntry(
            screen_view_ready_id="visual_first_screen_view_ready_001",
            screen_view_delivery_id=screen_view_delivery_entry.screen_view_delivery_id,
            screen_view_ready_mode="first_screen_view_ready",
            screen_view_ready_status="first_screen_view_ready_state",
            renderer_surface_id=screen_view_delivery_entry.renderer_surface_id,
            theme_id=screen_view_delivery_entry.theme_id,
            screen_id=screen_view_delivery_entry.screen_id,
            preview_artifact_id=screen_view_delivery_entry.preview_artifact_id,
            screen_view_delivery_ready=screen_view_delivery_entry.screen_view_delivery_ready,
            screen_view_ready=True,
            truth_bound_screen_view_ready=True,
            read_only=True,
            description=(
                "Canonical first screen-view ready entry after assembly of "
                "the first truth-preserving screen-view delivery."
            ),
        ),
    )

    return VisualFirstScreenViewReadyContract(
        contract_id="visual_first_screen_view_ready_contract_001",
        total_entries=len(entries),
        ready_entries=sum(
            1
            for entry in entries
            if entry.screen_view_ready_status == "first_screen_view_ready_state"
        ),
        read_only_entries=sum(1 for entry in entries if entry.read_only),
        entries=entries,
    )

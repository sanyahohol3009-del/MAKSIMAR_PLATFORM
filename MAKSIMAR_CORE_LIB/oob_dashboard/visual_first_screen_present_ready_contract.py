from __future__ import annotations

from dataclasses import dataclass
from typing import Literal

from MAKSIMAR_CORE_LIB.oob_dashboard.visual_first_screen_present_delivery_contract import (
    build_visual_first_screen_present_delivery_contract,
)


ScreenPresentReadyMode = Literal[
    "first_screen_present_ready",
]

ScreenPresentReadyStatus = Literal[
    "first_screen_present_ready_state",
]


@dataclass(frozen=True, slots=True)
class VisualFirstScreenPresentReadyEntry:
    """Canonical first screen-present ready entry."""

    screen_present_ready_id: str
    screen_present_delivery_id: str
    screen_present_ready_mode: ScreenPresentReadyMode
    screen_present_ready_status: ScreenPresentReadyStatus
    renderer_surface_id: str
    theme_id: str
    screen_id: str
    preview_artifact_id: str
    screen_present_delivery_ready: bool
    screen_present_ready: bool
    truth_bound_screen_present_ready: bool
    read_only: bool
    description: str


@dataclass(frozen=True, slots=True)
class VisualFirstScreenPresentReadyContract:
    """Canonical first screen-present ready contract."""

    contract_id: str
    total_entries: int
    ready_entries: int
    read_only_entries: int
    entries: tuple[VisualFirstScreenPresentReadyEntry, ...]


def build_visual_first_screen_present_ready_contract(
) -> VisualFirstScreenPresentReadyContract:
    """Build canonical first screen-present ready contract."""
    screen_present_delivery_contract = build_visual_first_screen_present_delivery_contract()
    screen_present_delivery_entry = screen_present_delivery_contract.entries[0]

    entries = (
        VisualFirstScreenPresentReadyEntry(
            screen_present_ready_id="visual_first_screen_present_ready_001",
            screen_present_delivery_id=screen_present_delivery_entry.screen_present_delivery_id,
            screen_present_ready_mode="first_screen_present_ready",
            screen_present_ready_status="first_screen_present_ready_state",
            renderer_surface_id=screen_present_delivery_entry.renderer_surface_id,
            theme_id=screen_present_delivery_entry.theme_id,
            screen_id=screen_present_delivery_entry.screen_id,
            preview_artifact_id=screen_present_delivery_entry.preview_artifact_id,
            screen_present_delivery_ready=screen_present_delivery_entry.screen_present_delivery_ready,
            screen_present_ready=True,
            truth_bound_screen_present_ready=True,
            read_only=True,
            description=(
                "Canonical first screen-present ready entry after assembly of "
                "the first truth-preserving screen-present delivery."
            ),
        ),
    )

    return VisualFirstScreenPresentReadyContract(
        contract_id="visual_first_screen_present_ready_contract_001",
        total_entries=len(entries),
        ready_entries=sum(
            1
            for entry in entries
            if entry.screen_present_ready_status == "first_screen_present_ready_state"
        ),
        read_only_entries=sum(1 for entry in entries if entry.read_only),
        entries=entries,
    )

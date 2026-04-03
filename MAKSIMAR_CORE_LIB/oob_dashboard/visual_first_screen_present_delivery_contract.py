from __future__ import annotations

from dataclasses import dataclass
from typing import Literal

from MAKSIMAR_CORE_LIB.oob_dashboard.visual_first_screen_present_contract import (
    build_visual_first_screen_present_contract,
)


ScreenPresentDeliveryMode = Literal[
    "first_screen_present_delivery",
]

ScreenPresentDeliveryStatus = Literal[
    "first_screen_present_delivery_ready",
]


@dataclass(frozen=True, slots=True)
class VisualFirstScreenPresentDeliveryEntry:
    """Canonical first screen-present delivery entry."""

    screen_present_delivery_id: str
    screen_present_id: str
    screen_present_delivery_mode: ScreenPresentDeliveryMode
    screen_present_delivery_status: ScreenPresentDeliveryStatus
    renderer_surface_id: str
    theme_id: str
    screen_id: str
    preview_artifact_id: str
    screen_present_ready: bool
    screen_present_delivery_ready: bool
    truth_bound_screen_present_delivery: bool
    read_only: bool
    description: str


@dataclass(frozen=True, slots=True)
class VisualFirstScreenPresentDeliveryContract:
    """Canonical first screen-present delivery contract."""

    contract_id: str
    total_entries: int
    ready_entries: int
    read_only_entries: int
    entries: tuple[VisualFirstScreenPresentDeliveryEntry, ...]


def build_visual_first_screen_present_delivery_contract(
) -> VisualFirstScreenPresentDeliveryContract:
    """Build canonical first screen-present delivery contract."""
    screen_present_contract = build_visual_first_screen_present_contract()
    screen_present_entry = screen_present_contract.entries[0]

    entries = (
        VisualFirstScreenPresentDeliveryEntry(
            screen_present_delivery_id="visual_first_screen_present_delivery_001",
            screen_present_id=screen_present_entry.screen_present_id,
            screen_present_delivery_mode="first_screen_present_delivery",
            screen_present_delivery_status="first_screen_present_delivery_ready",
            renderer_surface_id=screen_present_entry.renderer_surface_id,
            theme_id=screen_present_entry.theme_id,
            screen_id=screen_present_entry.screen_id,
            preview_artifact_id=screen_present_entry.preview_artifact_id,
            screen_present_ready=screen_present_entry.screen_present_ready,
            screen_present_delivery_ready=True,
            truth_bound_screen_present_delivery=True,
            read_only=True,
            description=(
                "Canonical first screen-present delivery entry after assembly of "
                "the first truth-preserving screen present."
            ),
        ),
    )

    return VisualFirstScreenPresentDeliveryContract(
        contract_id="visual_first_screen_present_delivery_contract_001",
        total_entries=len(entries),
        ready_entries=sum(
            1
            for entry in entries
            if entry.screen_present_delivery_status
            == "first_screen_present_delivery_ready"
        ),
        read_only_entries=sum(1 for entry in entries if entry.read_only),
        entries=entries,
    )

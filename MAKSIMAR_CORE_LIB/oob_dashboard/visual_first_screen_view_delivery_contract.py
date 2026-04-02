from __future__ import annotations

from dataclasses import dataclass
from typing import Literal

from MAKSIMAR_CORE_LIB.oob_dashboard.visual_first_screen_view_contract import (
    build_visual_first_screen_view_contract,
)


ScreenViewDeliveryMode = Literal[
    "first_screen_view_delivery",
]

ScreenViewDeliveryStatus = Literal[
    "first_screen_view_delivery_ready",
]


@dataclass(frozen=True, slots=True)
class VisualFirstScreenViewDeliveryEntry:
    """Canonical first screen-view delivery entry."""

    screen_view_delivery_id: str
    screen_view_id: str
    screen_view_delivery_mode: ScreenViewDeliveryMode
    screen_view_delivery_status: ScreenViewDeliveryStatus
    renderer_surface_id: str
    theme_id: str
    screen_id: str
    preview_artifact_id: str
    screen_view_ready: bool
    screen_view_delivery_ready: bool
    truth_bound_screen_view_delivery: bool
    read_only: bool
    description: str


@dataclass(frozen=True, slots=True)
class VisualFirstScreenViewDeliveryContract:
    """Canonical first screen-view delivery contract."""

    contract_id: str
    total_entries: int
    ready_entries: int
    read_only_entries: int
    entries: tuple[VisualFirstScreenViewDeliveryEntry, ...]


def build_visual_first_screen_view_delivery_contract(
) -> VisualFirstScreenViewDeliveryContract:
    """Build canonical first screen-view delivery contract."""
    screen_view_contract = build_visual_first_screen_view_contract()
    screen_view_entry = screen_view_contract.entries[0]

    entries = (
        VisualFirstScreenViewDeliveryEntry(
            screen_view_delivery_id="visual_first_screen_view_delivery_001",
            screen_view_id=screen_view_entry.screen_view_id,
            screen_view_delivery_mode="first_screen_view_delivery",
            screen_view_delivery_status="first_screen_view_delivery_ready",
            renderer_surface_id=screen_view_entry.renderer_surface_id,
            theme_id=screen_view_entry.theme_id,
            screen_id=screen_view_entry.screen_id,
            preview_artifact_id=screen_view_entry.preview_artifact_id,
            screen_view_ready=screen_view_entry.screen_view_ready,
            screen_view_delivery_ready=True,
            truth_bound_screen_view_delivery=True,
            read_only=True,
            description=(
                "Canonical first screen-view delivery entry after assembly of "
                "the first truth-preserving screen view."
            ),
        ),
    )

    return VisualFirstScreenViewDeliveryContract(
        contract_id="visual_first_screen_view_delivery_contract_001",
        total_entries=len(entries),
        ready_entries=sum(
            1
            for entry in entries
            if entry.screen_view_delivery_status == "first_screen_view_delivery_ready"
        ),
        read_only_entries=sum(1 for entry in entries if entry.read_only),
        entries=entries,
    )

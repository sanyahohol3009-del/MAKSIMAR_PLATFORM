from __future__ import annotations

from dataclasses import dataclass
from typing import Literal

from MAKSIMAR_CORE_LIB.oob_dashboard.visual_first_screen_render_contract import (
    build_visual_first_screen_render_contract,
)


ScreenRenderDeliveryMode = Literal[
    "first_screen_render_delivery",
]

ScreenRenderDeliveryStatus = Literal[
    "first_screen_render_delivery_ready",
]


@dataclass(frozen=True, slots=True)
class VisualFirstScreenRenderDeliveryEntry:
    """Canonical first screen-render delivery entry."""

    screen_render_delivery_id: str
    screen_render_id: str
    screen_render_delivery_mode: ScreenRenderDeliveryMode
    screen_render_delivery_status: ScreenRenderDeliveryStatus
    renderer_surface_id: str
    theme_id: str
    screen_id: str
    preview_artifact_id: str
    screen_render_ready: bool
    screen_render_delivery_ready: bool
    truth_bound_screen_render_delivery: bool
    read_only: bool
    description: str


@dataclass(frozen=True, slots=True)
class VisualFirstScreenRenderDeliveryContract:
    """Canonical first screen-render delivery contract."""

    contract_id: str
    total_entries: int
    ready_entries: int
    read_only_entries: int
    entries: tuple[VisualFirstScreenRenderDeliveryEntry, ...]


def build_visual_first_screen_render_delivery_contract(
) -> VisualFirstScreenRenderDeliveryContract:
    """Build canonical first screen-render delivery contract."""
    screen_render_contract = build_visual_first_screen_render_contract()
    screen_render_entry = screen_render_contract.entries[0]

    entries = (
        VisualFirstScreenRenderDeliveryEntry(
            screen_render_delivery_id="visual_first_screen_render_delivery_001",
            screen_render_id=screen_render_entry.screen_render_id,
            screen_render_delivery_mode="first_screen_render_delivery",
            screen_render_delivery_status="first_screen_render_delivery_ready",
            renderer_surface_id=screen_render_entry.renderer_surface_id,
            theme_id=screen_render_entry.theme_id,
            screen_id=screen_render_entry.screen_id,
            preview_artifact_id=screen_render_entry.preview_artifact_id,
            screen_render_ready=screen_render_entry.screen_render_ready,
            screen_render_delivery_ready=True,
            truth_bound_screen_render_delivery=True,
            read_only=True,
            description=(
                "Canonical first screen-render delivery entry after assembly of "
                "the first truth-preserving screen render."
            ),
        ),
    )

    return VisualFirstScreenRenderDeliveryContract(
        contract_id="visual_first_screen_render_delivery_contract_001",
        total_entries=len(entries),
        ready_entries=sum(
            1
            for entry in entries
            if entry.screen_render_delivery_status == "first_screen_render_delivery_ready"
        ),
        read_only_entries=sum(1 for entry in entries if entry.read_only),
        entries=entries,
    )

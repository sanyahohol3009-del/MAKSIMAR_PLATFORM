from __future__ import annotations

from dataclasses import dataclass
from typing import Literal

from MAKSIMAR_CORE_LIB.oob_dashboard.visual_first_screen_render_delivery_contract import (
    build_visual_first_screen_render_delivery_contract,
)


ScreenRenderReadyMode = Literal[
    "first_screen_render_ready",
]

ScreenRenderReadyStatus = Literal[
    "first_screen_render_ready_state",
]


@dataclass(frozen=True, slots=True)
class VisualFirstScreenRenderReadyEntry:
    """Canonical first screen-render ready entry."""

    screen_render_ready_id: str
    screen_render_delivery_id: str
    screen_render_ready_mode: ScreenRenderReadyMode
    screen_render_ready_status: ScreenRenderReadyStatus
    renderer_surface_id: str
    theme_id: str
    screen_id: str
    preview_artifact_id: str
    screen_render_delivery_ready: bool
    screen_render_ready: bool
    truth_bound_screen_render_ready: bool
    read_only: bool
    description: str


@dataclass(frozen=True, slots=True)
class VisualFirstScreenRenderReadyContract:
    """Canonical first screen-render ready contract."""

    contract_id: str
    total_entries: int
    ready_entries: int
    read_only_entries: int
    entries: tuple[VisualFirstScreenRenderReadyEntry, ...]


def build_visual_first_screen_render_ready_contract(
) -> VisualFirstScreenRenderReadyContract:
    """Build canonical first screen-render ready contract."""
    screen_render_delivery_contract = build_visual_first_screen_render_delivery_contract()
    screen_render_delivery_entry = screen_render_delivery_contract.entries[0]

    entries = (
        VisualFirstScreenRenderReadyEntry(
            screen_render_ready_id="visual_first_screen_render_ready_001",
            screen_render_delivery_id=screen_render_delivery_entry.screen_render_delivery_id,
            screen_render_ready_mode="first_screen_render_ready",
            screen_render_ready_status="first_screen_render_ready_state",
            renderer_surface_id=screen_render_delivery_entry.renderer_surface_id,
            theme_id=screen_render_delivery_entry.theme_id,
            screen_id=screen_render_delivery_entry.screen_id,
            preview_artifact_id=screen_render_delivery_entry.preview_artifact_id,
            screen_render_delivery_ready=screen_render_delivery_entry.screen_render_delivery_ready,
            screen_render_ready=True,
            truth_bound_screen_render_ready=True,
            read_only=True,
            description=(
                "Canonical first screen-render ready entry after assembly of "
                "the first truth-preserving screen-render delivery."
            ),
        ),
    )

    return VisualFirstScreenRenderReadyContract(
        contract_id="visual_first_screen_render_ready_contract_001",
        total_entries=len(entries),
        ready_entries=sum(
            1
            for entry in entries
            if entry.screen_render_ready_status == "first_screen_render_ready_state"
        ),
        read_only_entries=sum(1 for entry in entries if entry.read_only),
        entries=entries,
    )

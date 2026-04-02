from __future__ import annotations

from dataclasses import dataclass
from typing import Literal

from MAKSIMAR_CORE_LIB.oob_dashboard.visual_first_screen_view_ready_contract import (
    build_visual_first_screen_view_ready_contract,
)


ScreenRenderMode = Literal[
    "first_screen_render",
]

ScreenRenderStatus = Literal[
    "first_screen_render_ready",
]


@dataclass(frozen=True, slots=True)
class VisualFirstScreenRenderEntry:
    """Canonical first screen-render entry."""

    screen_render_id: str
    screen_view_ready_id: str
    screen_render_mode: ScreenRenderMode
    screen_render_status: ScreenRenderStatus
    renderer_surface_id: str
    theme_id: str
    screen_id: str
    preview_artifact_id: str
    screen_view_ready: bool
    screen_render_ready: bool
    truth_bound_screen_render: bool
    read_only: bool
    description: str


@dataclass(frozen=True, slots=True)
class VisualFirstScreenRenderContract:
    """Canonical first screen-render contract."""

    contract_id: str
    total_entries: int
    ready_entries: int
    read_only_entries: int
    entries: tuple[VisualFirstScreenRenderEntry, ...]


def build_visual_first_screen_render_contract() -> VisualFirstScreenRenderContract:
    """Build canonical first screen-render contract."""
    screen_view_ready_contract = build_visual_first_screen_view_ready_contract()
    screen_view_ready_entry = screen_view_ready_contract.entries[0]

    entries = (
        VisualFirstScreenRenderEntry(
            screen_render_id="visual_first_screen_render_001",
            screen_view_ready_id=screen_view_ready_entry.screen_view_ready_id,
            screen_render_mode="first_screen_render",
            screen_render_status="first_screen_render_ready",
            renderer_surface_id=screen_view_ready_entry.renderer_surface_id,
            theme_id=screen_view_ready_entry.theme_id,
            screen_id=screen_view_ready_entry.screen_id,
            preview_artifact_id=screen_view_ready_entry.preview_artifact_id,
            screen_view_ready=screen_view_ready_entry.screen_view_ready,
            screen_render_ready=True,
            truth_bound_screen_render=True,
            read_only=True,
            description=(
                "Canonical first screen-render entry after assembly of "
                "the first truth-preserving screen-view ready layer."
            ),
        ),
    )

    return VisualFirstScreenRenderContract(
        contract_id="visual_first_screen_render_contract_001",
        total_entries=len(entries),
        ready_entries=sum(
            1 for entry in entries if entry.screen_render_status == "first_screen_render_ready"
        ),
        read_only_entries=sum(1 for entry in entries if entry.read_only),
        entries=entries,
    )

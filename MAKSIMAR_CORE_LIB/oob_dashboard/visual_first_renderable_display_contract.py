from __future__ import annotations

from dataclasses import dataclass
from typing import Literal

from MAKSIMAR_CORE_LIB.oob_dashboard.visual_first_presented_display_contract import (
    build_visual_first_presented_display_contract,
)


RenderableDisplayMode = Literal[
    "first_renderable_display",
]

RenderableDisplayStatus = Literal[
    "renderable_display_ready",
]


@dataclass(frozen=True, slots=True)
class VisualFirstRenderableDisplayEntry:
    """Canonical first renderable display entry."""

    renderable_display_id: str
    presented_display_id: str
    renderable_display_mode: RenderableDisplayMode
    renderable_display_status: RenderableDisplayStatus
    renderer_surface_id: str
    theme_id: str
    screen_id: str
    preview_artifact_id: str
    presented_display_ready: bool
    renderable_display_ready: bool
    truth_bound_renderable_display: bool
    read_only: bool
    description: str


@dataclass(frozen=True, slots=True)
class VisualFirstRenderableDisplayContract:
    """Canonical first renderable display contract."""

    contract_id: str
    total_entries: int
    ready_entries: int
    read_only_entries: int
    entries: tuple[VisualFirstRenderableDisplayEntry, ...]


def build_visual_first_renderable_display_contract() -> VisualFirstRenderableDisplayContract:
    """Build canonical first renderable display contract."""
    presented_display_contract = build_visual_first_presented_display_contract()
    presented_display_entry = presented_display_contract.entries[0]

    entries = (
        VisualFirstRenderableDisplayEntry(
            renderable_display_id="visual_first_renderable_display_001",
            presented_display_id=presented_display_entry.presented_display_id,
            renderable_display_mode="first_renderable_display",
            renderable_display_status="renderable_display_ready",
            renderer_surface_id=presented_display_entry.renderer_surface_id,
            theme_id=presented_display_entry.theme_id,
            screen_id=presented_display_entry.screen_id,
            preview_artifact_id=presented_display_entry.preview_artifact_id,
            presented_display_ready=presented_display_entry.presented_display_ready,
            renderable_display_ready=True,
            truth_bound_renderable_display=True,
            read_only=True,
            description=(
                "Canonical first renderable display entry after assembly of "
                "the first truth-preserving presented display."
            ),
        ),
    )

    return VisualFirstRenderableDisplayContract(
        contract_id="visual_first_renderable_display_contract_001",
        total_entries=len(entries),
        ready_entries=sum(
            1
            for entry in entries
            if entry.renderable_display_status == "renderable_display_ready"
        ),
        read_only_entries=sum(1 for entry in entries if entry.read_only),
        entries=entries,
    )

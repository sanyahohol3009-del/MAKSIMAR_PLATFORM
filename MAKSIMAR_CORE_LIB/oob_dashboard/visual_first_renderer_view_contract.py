from __future__ import annotations

from dataclasses import dataclass
from typing import Literal

from MAKSIMAR_CORE_LIB.oob_dashboard.visual_first_renderer_realization_contract import (
    build_visual_first_renderer_realization_contract,
)


RendererViewMode = Literal[
    "first_renderer_view",
]

RendererViewStatus = Literal[
    "first_renderer_view_ready",
]


@dataclass(frozen=True, slots=True)
class VisualFirstRendererViewEntry:
    """Canonical first renderer view entry."""

    renderer_view_id: str
    renderer_realization_id: str
    renderer_view_mode: RendererViewMode
    renderer_view_status: RendererViewStatus
    renderer_surface_id: str
    theme_id: str
    screen_id: str
    preview_artifact_id: str
    renderer_realization_ready: bool
    renderer_view_ready: bool
    truth_bound_renderer_view: bool
    read_only: bool
    description: str


@dataclass(frozen=True, slots=True)
class VisualFirstRendererViewContract:
    """Canonical first renderer view contract."""

    contract_id: str
    total_entries: int
    ready_entries: int
    read_only_entries: int
    entries: tuple[VisualFirstRendererViewEntry, ...]


def build_visual_first_renderer_view_contract(
) -> VisualFirstRendererViewContract:
    """Build canonical first renderer view contract."""
    renderer_realization_contract = build_visual_first_renderer_realization_contract()
    renderer_realization_entry = renderer_realization_contract.entries[0]

    entries = (
        VisualFirstRendererViewEntry(
            renderer_view_id="visual_first_renderer_view_001",
            renderer_realization_id=renderer_realization_entry.renderer_realization_id,
            renderer_view_mode="first_renderer_view",
            renderer_view_status="first_renderer_view_ready",
            renderer_surface_id=renderer_realization_entry.renderer_surface_id,
            theme_id=renderer_realization_entry.theme_id,
            screen_id=renderer_realization_entry.screen_id,
            preview_artifact_id=renderer_realization_entry.preview_artifact_id,
            renderer_realization_ready=renderer_realization_entry.renderer_realization_ready,
            renderer_view_ready=True,
            truth_bound_renderer_view=True,
            read_only=True,
            description=(
                "Canonical first renderer view entry after assembly of "
                "the first truth-preserving renderer realization."
            ),
        ),
    )

    return VisualFirstRendererViewContract(
        contract_id="visual_first_renderer_view_contract_001",
        total_entries=len(entries),
        ready_entries=sum(
            1
            for entry in entries
            if entry.renderer_view_status == "first_renderer_view_ready"
        ),
        read_only_entries=sum(1 for entry in entries if entry.read_only),
        entries=entries,
    )

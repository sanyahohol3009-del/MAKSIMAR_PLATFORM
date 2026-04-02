from __future__ import annotations

from dataclasses import dataclass
from typing import Literal

from MAKSIMAR_CORE_LIB.oob_dashboard.visual_first_renderer_view_delivery_contract import (
    build_visual_first_renderer_view_delivery_contract,
)


RendererViewReadyMode = Literal[
    "first_renderer_view_ready",
]

RendererViewReadyStatus = Literal[
    "first_renderer_view_ready_state",
]


@dataclass(frozen=True, slots=True)
class VisualFirstRendererViewReadyEntry:
    """Canonical first renderer-view ready entry."""

    renderer_view_ready_id: str
    renderer_view_delivery_id: str
    renderer_view_ready_mode: RendererViewReadyMode
    renderer_view_ready_status: RendererViewReadyStatus
    renderer_surface_id: str
    theme_id: str
    screen_id: str
    preview_artifact_id: str
    renderer_view_delivery_ready: bool
    renderer_view_ready: bool
    truth_bound_renderer_view_ready: bool
    read_only: bool
    description: str


@dataclass(frozen=True, slots=True)
class VisualFirstRendererViewReadyContract:
    """Canonical first renderer-view ready contract."""

    contract_id: str
    total_entries: int
    ready_entries: int
    read_only_entries: int
    entries: tuple[VisualFirstRendererViewReadyEntry, ...]


def build_visual_first_renderer_view_ready_contract(
) -> VisualFirstRendererViewReadyContract:
    """Build canonical first renderer-view ready contract."""
    renderer_view_delivery_contract = (
        build_visual_first_renderer_view_delivery_contract()
    )
    renderer_view_delivery_entry = renderer_view_delivery_contract.entries[0]

    entries = (
        VisualFirstRendererViewReadyEntry(
            renderer_view_ready_id="visual_first_renderer_view_ready_001",
            renderer_view_delivery_id=(
                renderer_view_delivery_entry.renderer_view_delivery_id
            ),
            renderer_view_ready_mode="first_renderer_view_ready",
            renderer_view_ready_status="first_renderer_view_ready_state",
            renderer_surface_id=renderer_view_delivery_entry.renderer_surface_id,
            theme_id=renderer_view_delivery_entry.theme_id,
            screen_id=renderer_view_delivery_entry.screen_id,
            preview_artifact_id=renderer_view_delivery_entry.preview_artifact_id,
            renderer_view_delivery_ready=(
                renderer_view_delivery_entry.renderer_view_delivery_ready
            ),
            renderer_view_ready=True,
            truth_bound_renderer_view_ready=True,
            read_only=True,
            description=(
                "Canonical first renderer-view ready entry after assembly of "
                "the first truth-preserving renderer-view delivery."
            ),
        ),
    )

    return VisualFirstRendererViewReadyContract(
        contract_id="visual_first_renderer_view_ready_contract_001",
        total_entries=len(entries),
        ready_entries=sum(
            1
            for entry in entries
            if entry.renderer_view_ready_status == "first_renderer_view_ready_state"
        ),
        read_only_entries=sum(1 for entry in entries if entry.read_only),
        entries=entries,
    )

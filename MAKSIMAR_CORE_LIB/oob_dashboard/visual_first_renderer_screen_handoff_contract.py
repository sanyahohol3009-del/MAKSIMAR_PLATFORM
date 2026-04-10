from __future__ import annotations

from dataclasses import dataclass
from typing import Literal

from MAKSIMAR_CORE_LIB.oob_dashboard.visual_first_renderer_view_contract import (
    build_visual_first_renderer_view_contract,
)


RendererScreenHandoffMode = Literal[
    "first_renderer_screen_handoff",
]

RendererScreenHandoffStatus = Literal[
    "first_renderer_screen_handoff_ready",
]


@dataclass(frozen=True, slots=True)
class VisualFirstRendererScreenHandoffEntry:
    """Canonical first renderer-screen handoff entry."""

    renderer_screen_handoff_id: str
    renderer_view_id: str
    renderer_screen_handoff_mode: RendererScreenHandoffMode
    renderer_screen_handoff_status: RendererScreenHandoffStatus
    renderer_surface_id: str
    theme_id: str
    screen_id: str
    preview_artifact_id: str
    renderer_view_ready: bool
    renderer_screen_handoff_ready: bool
    truth_bound_renderer_screen_handoff: bool
    read_only: bool
    description: str


@dataclass(frozen=True, slots=True)
class VisualFirstRendererScreenHandoffContract:
    """Canonical first renderer-screen handoff contract."""

    contract_id: str
    total_entries: int
    ready_entries: int
    read_only_entries: int
    entries: tuple[VisualFirstRendererScreenHandoffEntry, ...]


def build_visual_first_renderer_screen_handoff_contract(
) -> VisualFirstRendererScreenHandoffContract:
    """Build canonical first renderer-screen handoff contract."""
    renderer_view_contract = build_visual_first_renderer_view_contract()
    renderer_view_entry = renderer_view_contract.entries[0]

    entries = (
        VisualFirstRendererScreenHandoffEntry(
            renderer_screen_handoff_id="visual_first_renderer_screen_handoff_001",
            renderer_view_id=renderer_view_entry.renderer_view_id,
            renderer_screen_handoff_mode="first_renderer_screen_handoff",
            renderer_screen_handoff_status="first_renderer_screen_handoff_ready",
            renderer_surface_id=renderer_view_entry.renderer_surface_id,
            theme_id=renderer_view_entry.theme_id,
            screen_id=renderer_view_entry.screen_id,
            preview_artifact_id=renderer_view_entry.preview_artifact_id,
            renderer_view_ready=renderer_view_entry.renderer_view_ready,
            renderer_screen_handoff_ready=True,
            truth_bound_renderer_screen_handoff=True,
            read_only=True,
            description=(
                "Canonical first renderer-screen handoff entry after assembly "
                "of the first truth-preserving renderer view."
            ),
        ),
    )

    return VisualFirstRendererScreenHandoffContract(
        contract_id="visual_first_renderer_screen_handoff_contract_001",
        total_entries=len(entries),
        ready_entries=sum(
            1
            for entry in entries
            if entry.renderer_screen_handoff_status
            == "first_renderer_screen_handoff_ready"
        ),
        read_only_entries=sum(1 for entry in entries if entry.read_only),
        entries=entries,
    )

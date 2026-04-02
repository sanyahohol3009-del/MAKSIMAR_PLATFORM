from __future__ import annotations

from dataclasses import dataclass
from typing import Literal

from MAKSIMAR_CORE_LIB.oob_dashboard.visual_first_renderer_screen_handoff_contract import (
    build_visual_first_renderer_screen_handoff_contract,
)


ScreenViewMode = Literal[
    "first_screen_view",
]

ScreenViewStatus = Literal[
    "first_screen_view_ready",
]


@dataclass(frozen=True, slots=True)
class VisualFirstScreenViewEntry:
    """Canonical first screen-view entry."""

    screen_view_id: str
    renderer_screen_handoff_id: str
    screen_view_mode: ScreenViewMode
    screen_view_status: ScreenViewStatus
    renderer_surface_id: str
    theme_id: str
    screen_id: str
    preview_artifact_id: str
    renderer_screen_handoff_ready: bool
    screen_view_ready: bool
    truth_bound_screen_view: bool
    read_only: bool
    description: str


@dataclass(frozen=True, slots=True)
class VisualFirstScreenViewContract:
    """Canonical first screen-view contract."""

    contract_id: str
    total_entries: int
    ready_entries: int
    read_only_entries: int
    entries: tuple[VisualFirstScreenViewEntry, ...]


def build_visual_first_screen_view_contract() -> VisualFirstScreenViewContract:
    """Build canonical first screen-view contract."""
    renderer_screen_handoff_contract = (
        build_visual_first_renderer_screen_handoff_contract()
    )
    renderer_screen_handoff_entry = renderer_screen_handoff_contract.entries[0]

    entries = (
        VisualFirstScreenViewEntry(
            screen_view_id="visual_first_screen_view_001",
            renderer_screen_handoff_id=(
                renderer_screen_handoff_entry.renderer_screen_handoff_id
            ),
            screen_view_mode="first_screen_view",
            screen_view_status="first_screen_view_ready",
            renderer_surface_id=renderer_screen_handoff_entry.renderer_surface_id,
            theme_id=renderer_screen_handoff_entry.theme_id,
            screen_id=renderer_screen_handoff_entry.screen_id,
            preview_artifact_id=renderer_screen_handoff_entry.preview_artifact_id,
            renderer_screen_handoff_ready=(
                renderer_screen_handoff_entry.renderer_screen_handoff_ready
            ),
            screen_view_ready=True,
            truth_bound_screen_view=True,
            read_only=True,
            description=(
                "Canonical first screen-view entry after assembly of the "
                "first truth-preserving renderer-screen handoff."
            ),
        ),
    )

    return VisualFirstScreenViewContract(
        contract_id="visual_first_screen_view_contract_001",
        total_entries=len(entries),
        ready_entries=sum(
            1 for entry in entries if entry.screen_view_status == "first_screen_view_ready"
        ),
        read_only_entries=sum(1 for entry in entries if entry.read_only),
        entries=entries,
    )

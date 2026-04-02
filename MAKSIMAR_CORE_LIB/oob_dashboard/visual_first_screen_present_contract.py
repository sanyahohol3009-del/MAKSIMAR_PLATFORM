from __future__ import annotations

from dataclasses import dataclass
from typing import Literal

from MAKSIMAR_CORE_LIB.oob_dashboard.visual_first_screen_render_ready_contract import (
    build_visual_first_screen_render_ready_contract,
)


ScreenPresentMode = Literal[
    "first_screen_present",
]

ScreenPresentStatus = Literal[
    "first_screen_present_ready",
]


@dataclass(frozen=True, slots=True)
class VisualFirstScreenPresentEntry:
    """Canonical first screen-present entry."""

    screen_present_id: str
    screen_render_ready_id: str
    screen_present_mode: ScreenPresentMode
    screen_present_status: ScreenPresentStatus
    renderer_surface_id: str
    theme_id: str
    screen_id: str
    preview_artifact_id: str
    screen_render_ready: bool
    screen_present_ready: bool
    truth_bound_screen_present: bool
    read_only: bool
    description: str


@dataclass(frozen=True, slots=True)
class VisualFirstScreenPresentContract:
    """Canonical first screen-present contract."""

    contract_id: str
    total_entries: int
    ready_entries: int
    read_only_entries: int
    entries: tuple[VisualFirstScreenPresentEntry, ...]


def build_visual_first_screen_present_contract() -> VisualFirstScreenPresentContract:
    """Build canonical first screen-present contract."""
    screen_render_ready_contract = build_visual_first_screen_render_ready_contract()
    screen_render_ready_entry = screen_render_ready_contract.entries[0]

    entries = (
        VisualFirstScreenPresentEntry(
            screen_present_id="visual_first_screen_present_001",
            screen_render_ready_id=screen_render_ready_entry.screen_render_ready_id,
            screen_present_mode="first_screen_present",
            screen_present_status="first_screen_present_ready",
            renderer_surface_id=screen_render_ready_entry.renderer_surface_id,
            theme_id=screen_render_ready_entry.theme_id,
            screen_id=screen_render_ready_entry.screen_id,
            preview_artifact_id=screen_render_ready_entry.preview_artifact_id,
            screen_render_ready=screen_render_ready_entry.screen_render_ready,
            screen_present_ready=True,
            truth_bound_screen_present=True,
            read_only=True,
            description=(
                "Canonical first screen-present entry after assembly of "
                "the first truth-preserving screen-render ready layer."
            ),
        ),
    )

    return VisualFirstScreenPresentContract(
        contract_id="visual_first_screen_present_contract_001",
        total_entries=len(entries),
        ready_entries=sum(
            1
            for entry in entries
            if entry.screen_present_status == "first_screen_present_ready"
        ),
        read_only_entries=sum(1 for entry in entries if entry.read_only),
        entries=entries,
    )

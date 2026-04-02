from __future__ import annotations

from dataclasses import dataclass
from typing import Literal

from MAKSIMAR_CORE_LIB.oob_dashboard.visual_first_demo_display_contract import (
    build_visual_first_demo_display_contract,
)


WatchableDisplayMode = Literal[
    "first_watchable_display",
]

WatchableDisplayStatus = Literal[
    "watchable_display_ready",
]


@dataclass(frozen=True, slots=True)
class VisualFirstWatchableDisplayEntry:
    """Canonical first watchable display entry."""

    watchable_display_id: str
    demo_display_id: str
    watchable_display_mode: WatchableDisplayMode
    watchable_display_status: WatchableDisplayStatus
    renderer_surface_id: str
    theme_id: str
    screen_id: str
    preview_artifact_id: str
    demo_display_ready: bool
    watchable_display_ready: bool
    truth_bound_watchable_display: bool
    read_only: bool
    description: str


@dataclass(frozen=True, slots=True)
class VisualFirstWatchableDisplayContract:
    """Canonical first watchable display contract."""

    contract_id: str
    total_entries: int
    ready_entries: int
    read_only_entries: int
    entries: tuple[VisualFirstWatchableDisplayEntry, ...]


def build_visual_first_watchable_display_contract(
) -> VisualFirstWatchableDisplayContract:
    """Build canonical first watchable display contract."""
    demo_display_contract = build_visual_first_demo_display_contract()
    demo_display_entry = demo_display_contract.entries[0]

    entries = (
        VisualFirstWatchableDisplayEntry(
            watchable_display_id="visual_first_watchable_display_001",
            demo_display_id=demo_display_entry.demo_display_id,
            watchable_display_mode="first_watchable_display",
            watchable_display_status="watchable_display_ready",
            renderer_surface_id=demo_display_entry.renderer_surface_id,
            theme_id=demo_display_entry.theme_id,
            screen_id=demo_display_entry.screen_id,
            preview_artifact_id=demo_display_entry.preview_artifact_id,
            demo_display_ready=demo_display_entry.demo_display_ready,
            watchable_display_ready=True,
            truth_bound_watchable_display=True,
            read_only=True,
            description=(
                "Canonical first watchable display entry after assembly of "
                "the first truth-preserving demo display."
            ),
        ),
    )

    return VisualFirstWatchableDisplayContract(
        contract_id="visual_first_watchable_display_contract_001",
        total_entries=len(entries),
        ready_entries=sum(
            1
            for entry in entries
            if entry.watchable_display_status == "watchable_display_ready"
        ),
        read_only_entries=sum(1 for entry in entries if entry.read_only),
        entries=entries,
    )

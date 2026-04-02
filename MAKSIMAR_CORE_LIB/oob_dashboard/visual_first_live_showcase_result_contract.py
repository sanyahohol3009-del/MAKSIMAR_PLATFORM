from __future__ import annotations

from dataclasses import dataclass
from typing import Literal

from MAKSIMAR_CORE_LIB.oob_dashboard.visual_first_live_screen_result_contract import (
    build_visual_first_live_screen_result_contract,
)


LiveShowcaseResultMode = Literal[
    "first_live_showcase_result",
]

LiveShowcaseResultStatus = Literal[
    "live_showcase_result_ready",
]


@dataclass(frozen=True, slots=True)
class VisualFirstLiveShowcaseResultEntry:
    """Canonical first live showcase result entry."""

    live_showcase_result_id: str
    live_screen_result_id: str
    live_showcase_result_mode: LiveShowcaseResultMode
    live_showcase_result_status: LiveShowcaseResultStatus
    renderer_surface_id: str
    theme_id: str
    screen_id: str
    preview_artifact_id: str
    live_screen_result_ready: bool
    live_showcase_result_ready: bool
    truth_bound_live_showcase_result: bool
    read_only: bool
    description: str


@dataclass(frozen=True, slots=True)
class VisualFirstLiveShowcaseResultContract:
    """Canonical first live showcase result contract."""

    contract_id: str
    total_entries: int
    ready_entries: int
    read_only_entries: int
    entries: tuple[VisualFirstLiveShowcaseResultEntry, ...]


def build_visual_first_live_showcase_result_contract(
) -> VisualFirstLiveShowcaseResultContract:
    """Build canonical first live showcase result contract."""
    live_screen_result_contract = build_visual_first_live_screen_result_contract()
    live_screen_result_entry = live_screen_result_contract.entries[0]

    entries = (
        VisualFirstLiveShowcaseResultEntry(
            live_showcase_result_id="visual_first_live_showcase_result_001",
            live_screen_result_id=live_screen_result_entry.live_screen_result_id,
            live_showcase_result_mode="first_live_showcase_result",
            live_showcase_result_status="live_showcase_result_ready",
            renderer_surface_id=live_screen_result_entry.renderer_surface_id,
            theme_id=live_screen_result_entry.theme_id,
            screen_id=live_screen_result_entry.screen_id,
            preview_artifact_id=live_screen_result_entry.preview_artifact_id,
            live_screen_result_ready=live_screen_result_entry.live_screen_result_ready,
            live_showcase_result_ready=True,
            truth_bound_live_showcase_result=True,
            read_only=True,
            description=(
                "Canonical first live showcase result entry after assembly of "
                "the first truth-preserving live screen result."
            ),
        ),
    )

    return VisualFirstLiveShowcaseResultContract(
        contract_id="visual_first_live_showcase_result_contract_001",
        total_entries=len(entries),
        ready_entries=sum(
            1
            for entry in entries
            if entry.live_showcase_result_status == "live_showcase_result_ready"
        ),
        read_only_entries=sum(1 for entry in entries if entry.read_only),
        entries=entries,
    )

from __future__ import annotations

from dataclasses import dataclass
from typing import Literal


LiveScreenResultMode = Literal[
    "first_live_screen_result",
]

LiveScreenResultStatus = Literal[
    "live_screen_result_ready",
]


@dataclass(frozen=True, slots=True)
class VisualFirstLiveScreenResultEntry:
    """Canonical first live screen result entry."""

    live_screen_result_id: str
    live_presentable_result_id: str
    live_screen_result_mode: LiveScreenResultMode
    live_screen_result_status: LiveScreenResultStatus
    renderer_surface_id: str
    theme_id: str
    screen_id: str
    preview_artifact_id: str
    live_presentable_result_ready: bool
    live_screen_result_ready: bool
    truth_bound_live_screen_result: bool
    read_only: bool
    description: str


@dataclass(frozen=True, slots=True)
class VisualFirstLiveScreenResultContract:
    """Canonical first live screen result contract."""

    contract_id: str
    total_entries: int
    ready_entries: int
    read_only_entries: int
    entries: tuple[VisualFirstLiveScreenResultEntry, ...]


def build_visual_first_live_screen_result_contract(
) -> VisualFirstLiveScreenResultContract:
    """Build canonical first live screen result contract."""
    from MAKSIMAR_CORE_LIB.oob_dashboard.visual_first_live_presentable_result_contract import (
        build_visual_first_live_presentable_result_contract,
    )

    live_presentable_result_contract = (
        build_visual_first_live_presentable_result_contract()
    )
    live_presentable_result_entry = live_presentable_result_contract.entries[0]

    entries = (
        VisualFirstLiveScreenResultEntry(
            live_screen_result_id="visual_first_live_screen_result_001",
            live_presentable_result_id=(
                live_presentable_result_entry.live_presentable_result_id
            ),
            live_screen_result_mode="first_live_screen_result",
            live_screen_result_status="live_screen_result_ready",
            renderer_surface_id=live_presentable_result_entry.renderer_surface_id,
            theme_id=live_presentable_result_entry.theme_id,
            screen_id=live_presentable_result_entry.screen_id,
            preview_artifact_id=live_presentable_result_entry.preview_artifact_id,
            live_presentable_result_ready=(
                live_presentable_result_entry.live_presentable_result_ready
            ),
            live_screen_result_ready=True,
            truth_bound_live_screen_result=True,
            read_only=True,
            description=(
                "Canonical first live screen result entry after assembly of "
                "the first truth-preserving live-presentable result."
            ),
        ),
    )

    return VisualFirstLiveScreenResultContract(
        contract_id="visual_first_live_screen_result_contract_001",
        total_entries=len(entries),
        ready_entries=sum(
            1
            for entry in entries
            if entry.live_screen_result_status == "live_screen_result_ready"
        ),
        read_only_entries=sum(1 for entry in entries if entry.read_only),
        entries=entries,
    )

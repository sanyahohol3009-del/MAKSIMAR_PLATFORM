from __future__ import annotations

from dataclasses import dataclass
from typing import Literal

from MAKSIMAR_CORE_LIB.oob_dashboard.visual_first_presented_result_contract import (
    build_visual_first_presented_result_contract,
)


ScreenPresentableResultMode = Literal[
    "first_screen_presentable_result",
]

ScreenPresentableResultStatus = Literal[
    "screen_presentable_result_ready",
]


@dataclass(frozen=True, slots=True)
class VisualFirstScreenPresentableResultEntry:
    """Canonical first screen-presentable result entry."""

    screen_presentable_result_id: str
    presented_result_id: str
    screen_presentable_result_mode: ScreenPresentableResultMode
    screen_presentable_result_status: ScreenPresentableResultStatus
    renderer_surface_id: str
    theme_id: str
    screen_id: str
    preview_artifact_id: str
    presented_result_ready: bool
    screen_presentable_result_ready: bool
    truth_bound_screen_presentable_result: bool
    read_only: bool
    description: str


@dataclass(frozen=True, slots=True)
class VisualFirstScreenPresentableResultContract:
    """Canonical first screen-presentable result contract."""

    contract_id: str
    total_entries: int
    ready_entries: int
    read_only_entries: int
    entries: tuple[VisualFirstScreenPresentableResultEntry, ...]


def build_visual_first_screen_presentable_result_contract(
) -> VisualFirstScreenPresentableResultContract:
    """Build canonical first screen-presentable result contract."""
    presented_result_contract = build_visual_first_presented_result_contract()
    presented_result_entry = presented_result_contract.entries[0]

    entries = (
        VisualFirstScreenPresentableResultEntry(
            screen_presentable_result_id="visual_first_screen_presentable_result_001",
            presented_result_id=presented_result_entry.presented_result_id,
            screen_presentable_result_mode="first_screen_presentable_result",
            screen_presentable_result_status="screen_presentable_result_ready",
            renderer_surface_id=presented_result_entry.renderer_surface_id,
            theme_id=presented_result_entry.theme_id,
            screen_id=presented_result_entry.screen_id,
            preview_artifact_id=presented_result_entry.preview_artifact_id,
            presented_result_ready=presented_result_entry.presented_result_ready,
            screen_presentable_result_ready=True,
            truth_bound_screen_presentable_result=True,
            read_only=True,
            description=(
                "Canonical first screen-presentable result entry after assembly "
                "of the first truth-preserving presented result."
            ),
        ),
    )

    return VisualFirstScreenPresentableResultContract(
        contract_id="visual_first_screen_presentable_result_contract_001",
        total_entries=len(entries),
        ready_entries=sum(
            1
            for entry in entries
            if entry.screen_presentable_result_status
            == "screen_presentable_result_ready"
        ),
        read_only_entries=sum(1 for entry in entries if entry.read_only),
        entries=entries,
    )

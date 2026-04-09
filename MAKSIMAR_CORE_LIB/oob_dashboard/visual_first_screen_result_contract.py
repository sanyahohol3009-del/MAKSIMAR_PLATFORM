from __future__ import annotations

from dataclasses import dataclass
from typing import Literal

from MAKSIMAR_CORE_LIB.oob_dashboard.visual_first_screen_presentable_result_contract import (
    build_visual_first_screen_presentable_result_contract,
)


ScreenResultMode = Literal[
    "first_screen_result",
]

ScreenResultStatus = Literal[
    "screen_result_ready",
]


@dataclass(frozen=True, slots=True)
class VisualFirstScreenResultEntry:
    """Canonical first screen result entry."""

    screen_result_id: str
    screen_presentable_result_id: str
    screen_result_mode: ScreenResultMode
    screen_result_status: ScreenResultStatus
    renderer_surface_id: str
    theme_id: str
    screen_id: str
    preview_artifact_id: str
    screen_presentable_result_ready: bool
    screen_result_ready: bool
    truth_bound_screen_result: bool
    read_only: bool
    description: str


@dataclass(frozen=True, slots=True)
class VisualFirstScreenResultContract:
    """Canonical first screen result contract."""

    contract_id: str
    total_entries: int
    ready_entries: int
    read_only_entries: int
    entries: tuple[VisualFirstScreenResultEntry, ...]


def build_visual_first_screen_result_contract() -> VisualFirstScreenResultContract:
    """Build canonical first screen result contract."""
    screen_presentable_result_contract = (
        build_visual_first_screen_presentable_result_contract()
    )
    screen_presentable_result_entry = screen_presentable_result_contract.entries[0]

    entries = (
        VisualFirstScreenResultEntry(
            screen_result_id="visual_first_screen_result_001",
            screen_presentable_result_id=(
                screen_presentable_result_entry.screen_presentable_result_id
            ),
            screen_result_mode="first_screen_result",
            screen_result_status="screen_result_ready",
            renderer_surface_id=screen_presentable_result_entry.renderer_surface_id,
            theme_id=screen_presentable_result_entry.theme_id,
            screen_id=screen_presentable_result_entry.screen_id,
            preview_artifact_id=screen_presentable_result_entry.preview_artifact_id,
            screen_presentable_result_ready=(
                screen_presentable_result_entry.screen_presentable_result_ready
            ),
            screen_result_ready=True,
            truth_bound_screen_result=True,
            read_only=True,
            description=(
                "Canonical first screen result entry after assembly of the "
                "first truth-preserving screen-presentable result."
            ),
        ),
    )

    return VisualFirstScreenResultContract(
        contract_id="visual_first_screen_result_contract_001",
        total_entries=len(entries),
        ready_entries=sum(
            1
            for entry in entries
            if entry.screen_result_status == "screen_result_ready"
        ),
        read_only_entries=sum(1 for entry in entries if entry.read_only),
        entries=entries,
    )

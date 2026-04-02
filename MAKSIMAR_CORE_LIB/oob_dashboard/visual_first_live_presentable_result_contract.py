from __future__ import annotations

from dataclasses import dataclass
from typing import Literal

from MAKSIMAR_CORE_LIB.oob_dashboard.visual_first_showcase_result_contract import (
    build_visual_first_showcase_result_contract,
)


LivePresentableResultMode = Literal[
    "first_live_presentable_result",
]

LivePresentableResultStatus = Literal[
    "live_presentable_result_ready",
]


@dataclass(frozen=True, slots=True)
class VisualFirstLivePresentableResultEntry:
    """Canonical first live-presentable result entry."""

    live_presentable_result_id: str
    showcase_result_id: str
    live_presentable_result_mode: LivePresentableResultMode
    live_presentable_result_status: LivePresentableResultStatus
    renderer_surface_id: str
    theme_id: str
    screen_id: str
    preview_artifact_id: str
    showcase_result_ready: bool
    live_presentable_result_ready: bool
    truth_bound_live_presentable_result: bool
    read_only: bool
    description: str


@dataclass(frozen=True, slots=True)
class VisualFirstLivePresentableResultContract:
    """Canonical first live-presentable result contract."""

    contract_id: str
    total_entries: int
    ready_entries: int
    read_only_entries: int
    entries: tuple[VisualFirstLivePresentableResultEntry, ...]


def build_visual_first_live_presentable_result_contract(
) -> VisualFirstLivePresentableResultContract:
    """Build canonical first live-presentable result contract."""
    showcase_result_contract = build_visual_first_showcase_result_contract()
    showcase_result_entry = showcase_result_contract.entries[0]

    entries = (
        VisualFirstLivePresentableResultEntry(
            live_presentable_result_id="visual_first_live_presentable_result_001",
            showcase_result_id=showcase_result_entry.showcase_result_id,
            live_presentable_result_mode="first_live_presentable_result",
            live_presentable_result_status="live_presentable_result_ready",
            renderer_surface_id=showcase_result_entry.renderer_surface_id,
            theme_id=showcase_result_entry.theme_id,
            screen_id=showcase_result_entry.screen_id,
            preview_artifact_id=showcase_result_entry.preview_artifact_id,
            showcase_result_ready=showcase_result_entry.showcase_result_ready,
            live_presentable_result_ready=True,
            truth_bound_live_presentable_result=True,
            read_only=True,
            description=(
                "Canonical first live-presentable result entry after assembly "
                "of the first truth-preserving showcase result."
            ),
        ),
    )

    return VisualFirstLivePresentableResultContract(
        contract_id="visual_first_live_presentable_result_contract_001",
        total_entries=len(entries),
        ready_entries=sum(
            1
            for entry in entries
            if entry.live_presentable_result_status == "live_presentable_result_ready"
        ),
        read_only_entries=sum(1 for entry in entries if entry.read_only),
        entries=entries,
    )

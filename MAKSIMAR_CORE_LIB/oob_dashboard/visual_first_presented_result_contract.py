from __future__ import annotations

from dataclasses import dataclass
from typing import Literal

from MAKSIMAR_CORE_LIB.oob_dashboard.visual_first_presentable_result_contract import (
    build_visual_first_presentable_result_contract,
)


PresentedResultMode = Literal[
    "first_presented_result",
]

PresentedResultStatus = Literal[
    "presented_result_ready",
]


@dataclass(frozen=True, slots=True)
class VisualFirstPresentedResultEntry:
    """Canonical first presented result entry."""

    presented_result_id: str
    presentable_result_id: str
    presented_result_mode: PresentedResultMode
    presented_result_status: PresentedResultStatus
    renderer_surface_id: str
    theme_id: str
    screen_id: str
    preview_artifact_id: str
    presentable_result_ready: bool
    presented_result_ready: bool
    truth_bound_presented_result: bool
    read_only: bool
    description: str


@dataclass(frozen=True, slots=True)
class VisualFirstPresentedResultContract:
    """Canonical first presented result contract."""

    contract_id: str
    total_entries: int
    ready_entries: int
    read_only_entries: int
    entries: tuple[VisualFirstPresentedResultEntry, ...]


def build_visual_first_presented_result_contract(
) -> VisualFirstPresentedResultContract:
    """Build canonical first presented result contract."""
    presentable_result_contract = build_visual_first_presentable_result_contract()
    presentable_result_entry = presentable_result_contract.entries[0]

    entries = (
        VisualFirstPresentedResultEntry(
            presented_result_id="visual_first_presented_result_001",
            presentable_result_id=presentable_result_entry.presentable_result_id,
            presented_result_mode="first_presented_result",
            presented_result_status="presented_result_ready",
            renderer_surface_id=presentable_result_entry.renderer_surface_id,
            theme_id=presentable_result_entry.theme_id,
            screen_id=presentable_result_entry.screen_id,
            preview_artifact_id=presentable_result_entry.preview_artifact_id,
            presentable_result_ready=presentable_result_entry.presentable_result_ready,
            presented_result_ready=True,
            truth_bound_presented_result=True,
            read_only=True,
            description=(
                "Canonical first presented result entry after assembly of the "
                "first truth-preserving presentable result."
            ),
        ),
    )

    return VisualFirstPresentedResultContract(
        contract_id="visual_first_presented_result_contract_001",
        total_entries=len(entries),
        ready_entries=sum(
            1
            for entry in entries
            if entry.presented_result_status == "presented_result_ready"
        ),
        read_only_entries=sum(1 for entry in entries if entry.read_only),
        entries=entries,
    )

from __future__ import annotations

from dataclasses import dataclass
from typing import Literal

from MAKSIMAR_CORE_LIB.oob_dashboard.visual_first_result_display_contract import (
    build_visual_first_result_display_contract,
)


ViewableResultMode = Literal[
    "first_viewable_result",
]

ViewableResultStatus = Literal[
    "viewable_result_ready",
]


@dataclass(frozen=True, slots=True)
class VisualFirstViewableResultEntry:
    """Canonical first viewable result entry."""

    viewable_result_id: str
    result_display_id: str
    viewable_result_mode: ViewableResultMode
    viewable_result_status: ViewableResultStatus
    renderer_surface_id: str
    theme_id: str
    screen_id: str
    preview_artifact_id: str
    result_ready: bool
    viewable_result_ready: bool
    truth_bound_viewable_result: bool
    read_only: bool
    description: str


@dataclass(frozen=True, slots=True)
class VisualFirstViewableResultContract:
    """Canonical first viewable result contract."""

    contract_id: str
    total_entries: int
    ready_entries: int
    read_only_entries: int
    entries: tuple[VisualFirstViewableResultEntry, ...]


def build_visual_first_viewable_result_contract() -> VisualFirstViewableResultContract:
    """Build canonical first viewable result contract."""
    result_display_contract = build_visual_first_result_display_contract()
    result_display_entry = result_display_contract.entries[0]

    entries = (
        VisualFirstViewableResultEntry(
            viewable_result_id="visual_first_viewable_result_001",
            result_display_id=result_display_entry.result_display_id,
            viewable_result_mode="first_viewable_result",
            viewable_result_status="viewable_result_ready",
            renderer_surface_id=result_display_entry.renderer_surface_id,
            theme_id=result_display_entry.theme_id,
            screen_id=result_display_entry.screen_id,
            preview_artifact_id=result_display_entry.preview_artifact_id,
            result_ready=result_display_entry.result_ready,
            viewable_result_ready=True,
            truth_bound_viewable_result=True,
            read_only=True,
            description=(
                "Canonical first viewable result entry after assembly of the "
                "first truth-preserving result display."
            ),
        ),
    )

    return VisualFirstViewableResultContract(
        contract_id="visual_first_viewable_result_contract_001",
        total_entries=len(entries),
        ready_entries=sum(
            1
            for entry in entries
            if entry.viewable_result_status == "viewable_result_ready"
        ),
        read_only_entries=sum(1 for entry in entries if entry.read_only),
        entries=entries,
    )

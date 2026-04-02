from __future__ import annotations

from dataclasses import dataclass
from typing import Literal

from MAKSIMAR_CORE_LIB.oob_dashboard.visual_first_viewable_result_contract import (
    build_visual_first_viewable_result_contract,
)


DisplayOutputMode = Literal[
    "first_display_output",
]

DisplayOutputStatus = Literal[
    "display_output_ready",
]


@dataclass(frozen=True, slots=True)
class VisualFirstDisplayOutputEntry:
    """Canonical first display output entry."""

    display_output_id: str
    viewable_result_id: str
    display_output_mode: DisplayOutputMode
    display_output_status: DisplayOutputStatus
    renderer_surface_id: str
    theme_id: str
    screen_id: str
    preview_artifact_id: str
    viewable_result_ready: bool
    display_output_ready: bool
    truth_bound_display_output: bool
    read_only: bool
    description: str


@dataclass(frozen=True, slots=True)
class VisualFirstDisplayOutputContract:
    """Canonical first display output contract."""

    contract_id: str
    total_entries: int
    ready_entries: int
    read_only_entries: int
    entries: tuple[VisualFirstDisplayOutputEntry, ...]


def build_visual_first_display_output_contract() -> VisualFirstDisplayOutputContract:
    """Build canonical first display output contract."""
    viewable_result_contract = build_visual_first_viewable_result_contract()
    viewable_result_entry = viewable_result_contract.entries[0]

    entries = (
        VisualFirstDisplayOutputEntry(
            display_output_id="visual_first_display_output_001",
            viewable_result_id=viewable_result_entry.viewable_result_id,
            display_output_mode="first_display_output",
            display_output_status="display_output_ready",
            renderer_surface_id=viewable_result_entry.renderer_surface_id,
            theme_id=viewable_result_entry.theme_id,
            screen_id=viewable_result_entry.screen_id,
            preview_artifact_id=viewable_result_entry.preview_artifact_id,
            viewable_result_ready=viewable_result_entry.viewable_result_ready,
            display_output_ready=True,
            truth_bound_display_output=True,
            read_only=True,
            description=(
                "Canonical first display output entry after assembly of the "
                "first truth-preserving viewable result."
            ),
        ),
    )

    return VisualFirstDisplayOutputContract(
        contract_id="visual_first_display_output_contract_001",
        total_entries=len(entries),
        ready_entries=sum(
            1
            for entry in entries
            if entry.display_output_status == "display_output_ready"
        ),
        read_only_entries=sum(1 for entry in entries if entry.read_only),
        entries=entries,
    )

from __future__ import annotations

from dataclasses import dataclass
from typing import Literal

from MAKSIMAR_CORE_LIB.oob_dashboard.visual_first_output_ready_display_contract import (
    build_visual_first_output_ready_display_contract,
)


ResultDisplayMode = Literal[
    "first_result_display",
]

ResultDisplayStatus = Literal[
    "result_display_ready",
]


@dataclass(frozen=True, slots=True)
class VisualFirstResultDisplayEntry:
    """Canonical first result display entry."""

    result_display_id: str
    output_ready_display_id: str
    result_display_mode: ResultDisplayMode
    result_display_status: ResultDisplayStatus
    renderer_surface_id: str
    theme_id: str
    screen_id: str
    preview_artifact_id: str
    output_ready: bool
    result_ready: bool
    truth_bound_result_display: bool
    read_only: bool
    description: str


@dataclass(frozen=True, slots=True)
class VisualFirstResultDisplayContract:
    """Canonical first result display contract."""

    contract_id: str
    total_entries: int
    ready_entries: int
    read_only_entries: int
    entries: tuple[VisualFirstResultDisplayEntry, ...]


def build_visual_first_result_display_contract() -> VisualFirstResultDisplayContract:
    """Build canonical first result display contract."""
    output_ready_display_contract = build_visual_first_output_ready_display_contract()
    output_ready_display_entry = output_ready_display_contract.entries[0]

    entries = (
        VisualFirstResultDisplayEntry(
            result_display_id="visual_first_result_display_001",
            output_ready_display_id=output_ready_display_entry.output_ready_display_id,
            result_display_mode="first_result_display",
            result_display_status="result_display_ready",
            renderer_surface_id=output_ready_display_entry.renderer_surface_id,
            theme_id=output_ready_display_entry.theme_id,
            screen_id=output_ready_display_entry.screen_id,
            preview_artifact_id=output_ready_display_entry.preview_artifact_id,
            output_ready=output_ready_display_entry.output_ready,
            result_ready=True,
            truth_bound_result_display=True,
            read_only=True,
            description=(
                "Canonical first result display entry after assembly of the "
                "first truth-preserving output-ready display."
            ),
        ),
    )

    return VisualFirstResultDisplayContract(
        contract_id="visual_first_result_display_contract_001",
        total_entries=len(entries),
        ready_entries=sum(
            1
            for entry in entries
            if entry.result_display_status == "result_display_ready"
        ),
        read_only_entries=sum(1 for entry in entries if entry.read_only),
        entries=entries,
    )

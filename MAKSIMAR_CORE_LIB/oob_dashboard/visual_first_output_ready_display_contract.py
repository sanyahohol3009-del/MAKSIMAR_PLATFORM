from __future__ import annotations

from dataclasses import dataclass
from typing import Literal

from MAKSIMAR_CORE_LIB.oob_dashboard.visual_first_renderable_display_contract import (
    build_visual_first_renderable_display_contract,
)


OutputReadyDisplayMode = Literal[
    "first_output_ready_display",
]

OutputReadyDisplayStatus = Literal[
    "output_ready_display_ready",
]


@dataclass(frozen=True, slots=True)
class VisualFirstOutputReadyDisplayEntry:
    """Canonical first output-ready display entry."""

    output_ready_display_id: str
    renderable_display_id: str
    output_ready_display_mode: OutputReadyDisplayMode
    output_ready_display_status: OutputReadyDisplayStatus
    renderer_surface_id: str
    theme_id: str
    screen_id: str
    preview_artifact_id: str
    renderable_display_ready: bool
    output_ready: bool
    truth_bound_output_ready_display: bool
    read_only: bool
    description: str


@dataclass(frozen=True, slots=True)
class VisualFirstOutputReadyDisplayContract:
    """Canonical first output-ready display contract."""

    contract_id: str
    total_entries: int
    ready_entries: int
    read_only_entries: int
    entries: tuple[VisualFirstOutputReadyDisplayEntry, ...]


def build_visual_first_output_ready_display_contract(
) -> VisualFirstOutputReadyDisplayContract:
    """Build canonical first output-ready display contract."""
    renderable_display_contract = build_visual_first_renderable_display_contract()
    renderable_display_entry = renderable_display_contract.entries[0]

    entries = (
        VisualFirstOutputReadyDisplayEntry(
            output_ready_display_id="visual_first_output_ready_display_001",
            renderable_display_id=renderable_display_entry.renderable_display_id,
            output_ready_display_mode="first_output_ready_display",
            output_ready_display_status="output_ready_display_ready",
            renderer_surface_id=renderable_display_entry.renderer_surface_id,
            theme_id=renderable_display_entry.theme_id,
            screen_id=renderable_display_entry.screen_id,
            preview_artifact_id=renderable_display_entry.preview_artifact_id,
            renderable_display_ready=renderable_display_entry.renderable_display_ready,
            output_ready=True,
            truth_bound_output_ready_display=True,
            read_only=True,
            description=(
                "Canonical first output-ready display entry after assembly of "
                "the first truth-preserving renderable display."
            ),
        ),
    )

    return VisualFirstOutputReadyDisplayContract(
        contract_id="visual_first_output_ready_display_contract_001",
        total_entries=len(entries),
        ready_entries=sum(
            1
            for entry in entries
            if entry.output_ready_display_status == "output_ready_display_ready"
        ),
        read_only_entries=sum(1 for entry in entries if entry.read_only),
        entries=entries,
    )

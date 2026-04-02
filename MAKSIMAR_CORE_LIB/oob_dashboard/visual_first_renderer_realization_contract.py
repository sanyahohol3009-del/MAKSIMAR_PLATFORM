from __future__ import annotations

from dataclasses import dataclass
from typing import Literal

from MAKSIMAR_CORE_LIB.oob_dashboard.visual_premium_demo_first_picture_contract import (
    build_visual_premium_demo_first_picture_contract,
)


RendererRealizationMode = Literal[
    "first_renderer_realization",
]

RendererRealizationStatus = Literal[
    "first_renderer_realization_ready",
]


@dataclass(frozen=True, slots=True)
class VisualFirstRendererRealizationEntry:
    """Canonical first renderer realization entry."""

    renderer_realization_id: str
    first_picture_id: str
    renderer_realization_mode: RendererRealizationMode
    renderer_realization_status: RendererRealizationStatus
    renderer_surface_id: str
    theme_id: str
    screen_id: str
    preview_artifact_id: str
    first_picture_ready: bool
    renderer_realization_ready: bool
    truth_bound_renderer_realization: bool
    read_only: bool
    description: str


@dataclass(frozen=True, slots=True)
class VisualFirstRendererRealizationContract:
    """Canonical first renderer realization contract."""

    contract_id: str
    total_entries: int
    ready_entries: int
    read_only_entries: int
    entries: tuple[VisualFirstRendererRealizationEntry, ...]


def build_visual_first_renderer_realization_contract(
) -> VisualFirstRendererRealizationContract:
    """Build canonical first renderer realization contract."""
    first_picture_contract = build_visual_premium_demo_first_picture_contract()
    first_picture_entry = first_picture_contract.entries[0]

    entries = (
        VisualFirstRendererRealizationEntry(
            renderer_realization_id="visual_first_renderer_realization_001",
            first_picture_id=first_picture_entry.first_picture_id,
            renderer_realization_mode="first_renderer_realization",
            renderer_realization_status="first_renderer_realization_ready",
            renderer_surface_id=first_picture_entry.renderer_surface_id,
            theme_id=first_picture_entry.theme_id,
            screen_id=first_picture_entry.screen_id,
            preview_artifact_id=first_picture_entry.preview_artifact_id,
            first_picture_ready=first_picture_entry.first_picture_ready,
            renderer_realization_ready=True,
            truth_bound_renderer_realization=True,
            read_only=True,
            description=(
                "Canonical first renderer realization entry after assembly of "
                "the first truth-preserving premium demo first picture."
            ),
        ),
    )

    return VisualFirstRendererRealizationContract(
        contract_id="visual_first_renderer_realization_contract_001",
        total_entries=len(entries),
        ready_entries=sum(
            1
            for entry in entries
            if entry.renderer_realization_status == "first_renderer_realization_ready"
        ),
        read_only_entries=sum(1 for entry in entries if entry.read_only),
        entries=entries,
    )

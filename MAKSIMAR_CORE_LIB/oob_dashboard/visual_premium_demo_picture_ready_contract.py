from __future__ import annotations

from dataclasses import dataclass
from typing import Literal

from MAKSIMAR_CORE_LIB.oob_dashboard.visual_premium_demo_picture_boundary_contract import (
    build_visual_premium_demo_picture_boundary_contract,
)


PremiumDemoPictureReadyMode = Literal[
    "premium_demo_picture_ready",
]

PremiumDemoPictureReadyStatus = Literal[
    "premium_demo_picture_ready_state",
]


@dataclass(frozen=True, slots=True)
class VisualPremiumDemoPictureReadyEntry:
    """Canonical premium demo picture-ready entry."""

    picture_ready_id: str
    picture_boundary_id: str
    picture_ready_mode: PremiumDemoPictureReadyMode
    picture_ready_status: PremiumDemoPictureReadyStatus
    renderer_surface_id: str
    theme_id: str
    screen_id: str
    preview_artifact_id: str
    picture_boundary_ready: bool
    picture_ready: bool
    truth_bound_picture_ready: bool
    read_only: bool
    description: str


@dataclass(frozen=True, slots=True)
class VisualPremiumDemoPictureReadyContract:
    """Canonical premium demo picture-ready contract."""

    contract_id: str
    total_entries: int
    ready_entries: int
    read_only_entries: int
    entries: tuple[VisualPremiumDemoPictureReadyEntry, ...]


def build_visual_premium_demo_picture_ready_contract(
) -> VisualPremiumDemoPictureReadyContract:
    """Build canonical premium demo picture-ready contract."""
    picture_boundary_contract = build_visual_premium_demo_picture_boundary_contract()
    picture_boundary_entry = picture_boundary_contract.entries[0]

    entries = (
        VisualPremiumDemoPictureReadyEntry(
            picture_ready_id="visual_premium_demo_picture_ready_001",
            picture_boundary_id=picture_boundary_entry.picture_boundary_id,
            picture_ready_mode="premium_demo_picture_ready",
            picture_ready_status="premium_demo_picture_ready_state",
            renderer_surface_id=picture_boundary_entry.renderer_surface_id,
            theme_id=picture_boundary_entry.theme_id,
            screen_id=picture_boundary_entry.screen_id,
            preview_artifact_id=picture_boundary_entry.preview_artifact_id,
            picture_boundary_ready=picture_boundary_entry.picture_boundary_ready,
            picture_ready=True,
            truth_bound_picture_ready=True,
            read_only=True,
            description=(
                "Canonical premium demo picture-ready entry after assembly of "
                "the first truth-preserving premium demo picture boundary."
            ),
        ),
    )

    return VisualPremiumDemoPictureReadyContract(
        contract_id="visual_premium_demo_picture_ready_contract_001",
        total_entries=len(entries),
        ready_entries=sum(
            1
            for entry in entries
            if entry.picture_ready_status == "premium_demo_picture_ready_state"
        ),
        read_only_entries=sum(1 for entry in entries if entry.read_only),
        entries=entries,
    )

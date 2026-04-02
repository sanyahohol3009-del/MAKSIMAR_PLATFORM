from __future__ import annotations

from dataclasses import dataclass
from typing import Literal

from MAKSIMAR_CORE_LIB.oob_dashboard.visual_premium_demo_screen_delivery_contract import (
    build_visual_premium_demo_screen_delivery_contract,
)


PremiumDemoPictureBoundaryMode = Literal[
    "premium_demo_picture_boundary",
]

PremiumDemoPictureBoundaryStatus = Literal[
    "premium_demo_picture_boundary_ready",
]


@dataclass(frozen=True, slots=True)
class VisualPremiumDemoPictureBoundaryEntry:
    """Canonical premium demo picture boundary entry."""

    picture_boundary_id: str
    screen_delivery_id: str
    picture_boundary_mode: PremiumDemoPictureBoundaryMode
    picture_boundary_status: PremiumDemoPictureBoundaryStatus
    renderer_surface_id: str
    theme_id: str
    screen_id: str
    preview_artifact_id: str
    screen_delivery_ready: bool
    picture_boundary_ready: bool
    truth_bound_picture_boundary: bool
    read_only: bool
    description: str


@dataclass(frozen=True, slots=True)
class VisualPremiumDemoPictureBoundaryContract:
    """Canonical premium demo picture boundary contract."""

    contract_id: str
    total_entries: int
    ready_entries: int
    read_only_entries: int
    entries: tuple[VisualPremiumDemoPictureBoundaryEntry, ...]


def build_visual_premium_demo_picture_boundary_contract(
) -> VisualPremiumDemoPictureBoundaryContract:
    """Build canonical premium demo picture boundary contract."""
    screen_delivery_contract = build_visual_premium_demo_screen_delivery_contract()
    screen_delivery_entry = screen_delivery_contract.entries[0]

    entries = (
        VisualPremiumDemoPictureBoundaryEntry(
            picture_boundary_id="visual_premium_demo_picture_boundary_001",
            screen_delivery_id=screen_delivery_entry.screen_delivery_id,
            picture_boundary_mode="premium_demo_picture_boundary",
            picture_boundary_status="premium_demo_picture_boundary_ready",
            renderer_surface_id=screen_delivery_entry.renderer_surface_id,
            theme_id=screen_delivery_entry.theme_id,
            screen_id=screen_delivery_entry.screen_id,
            preview_artifact_id=screen_delivery_entry.preview_artifact_id,
            screen_delivery_ready=screen_delivery_entry.screen_delivery_ready,
            picture_boundary_ready=True,
            truth_bound_picture_boundary=True,
            read_only=True,
            description=(
                "Canonical premium demo picture boundary entry after assembly "
                "of the first truth-preserving premium demo screen delivery."
            ),
        ),
    )

    return VisualPremiumDemoPictureBoundaryContract(
        contract_id="visual_premium_demo_picture_boundary_contract_001",
        total_entries=len(entries),
        ready_entries=sum(
            1
            for entry in entries
            if entry.picture_boundary_status == "premium_demo_picture_boundary_ready"
        ),
        read_only_entries=sum(1 for entry in entries if entry.read_only),
        entries=entries,
    )

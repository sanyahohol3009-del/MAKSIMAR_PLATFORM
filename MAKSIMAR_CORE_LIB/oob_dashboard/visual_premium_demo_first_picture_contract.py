from __future__ import annotations

from dataclasses import dataclass
from typing import Literal

from MAKSIMAR_CORE_LIB.oob_dashboard.visual_premium_demo_materialized_output_contract import (
    build_visual_premium_demo_materialized_output_contract,
)


FirstPictureMode = Literal[
    "premium_demo_first_picture",
]

FirstPictureStatus = Literal[
    "premium_demo_first_picture_ready",
]


@dataclass(frozen=True, slots=True)
class VisualPremiumDemoFirstPictureEntry:
    """Canonical premium demo first picture entry."""

    first_picture_id: str
    materialized_output_id: str
    first_picture_mode: FirstPictureMode
    first_picture_status: FirstPictureStatus
    renderer_surface_id: str
    theme_id: str
    screen_id: str
    preview_artifact_id: str
    materialized_output_ready: bool
    first_picture_ready: bool
    truth_bound_first_picture: bool
    read_only: bool
    description: str


@dataclass(frozen=True, slots=True)
class VisualPremiumDemoFirstPictureContract:
    """Canonical premium demo first picture contract."""

    contract_id: str
    total_entries: int
    ready_entries: int
    read_only_entries: int
    entries: tuple[VisualPremiumDemoFirstPictureEntry, ...]


def build_visual_premium_demo_first_picture_contract(
) -> VisualPremiumDemoFirstPictureContract:
    """Build canonical premium demo first picture contract."""
    materialized_output_contract = build_visual_premium_demo_materialized_output_contract()
    materialized_output_entry = materialized_output_contract.entries[0]

    entries = (
        VisualPremiumDemoFirstPictureEntry(
            first_picture_id="visual_premium_demo_first_picture_001",
            materialized_output_id=materialized_output_entry.materialized_output_id,
            first_picture_mode="premium_demo_first_picture",
            first_picture_status="premium_demo_first_picture_ready",
            renderer_surface_id=materialized_output_entry.renderer_surface_id,
            theme_id=materialized_output_entry.theme_id,
            screen_id=materialized_output_entry.screen_id,
            preview_artifact_id=materialized_output_entry.preview_artifact_id,
            materialized_output_ready=materialized_output_entry.materialized_output_ready,
            first_picture_ready=True,
            truth_bound_first_picture=True,
            read_only=True,
            description=(
                "Canonical premium demo first picture entry after assembly of "
                "the first truth-preserving premium demo materialized output."
            ),
        ),
    )

    return VisualPremiumDemoFirstPictureContract(
        contract_id="visual_premium_demo_first_picture_contract_001",
        total_entries=len(entries),
        ready_entries=sum(
            1
            for entry in entries
            if entry.first_picture_status == "premium_demo_first_picture_ready"
        ),
        read_only_entries=sum(1 for entry in entries if entry.read_only),
        entries=entries,
    )

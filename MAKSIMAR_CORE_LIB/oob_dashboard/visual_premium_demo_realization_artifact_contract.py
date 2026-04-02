from __future__ import annotations

from dataclasses import dataclass
from typing import Literal

from MAKSIMAR_CORE_LIB.oob_dashboard.visual_premium_demo_picture_ready_contract import (
    build_visual_premium_demo_picture_ready_contract,
)


RealizationArtifactMode = Literal[
    "premium_demo_realization_artifact",
]

RealizationArtifactStatus = Literal[
    "premium_demo_realization_artifact_ready",
]


@dataclass(frozen=True, slots=True)
class VisualPremiumDemoRealizationArtifactEntry:
    """Canonical premium demo realization artifact entry."""

    realization_artifact_id: str
    picture_ready_id: str
    realization_artifact_mode: RealizationArtifactMode
    realization_artifact_status: RealizationArtifactStatus
    renderer_surface_id: str
    theme_id: str
    screen_id: str
    preview_artifact_id: str
    picture_ready: bool
    realization_artifact_ready: bool
    truth_bound_realization_artifact: bool
    read_only: bool
    description: str


@dataclass(frozen=True, slots=True)
class VisualPremiumDemoRealizationArtifactContract:
    """Canonical premium demo realization artifact contract."""

    contract_id: str
    total_entries: int
    ready_entries: int
    read_only_entries: int
    entries: tuple[VisualPremiumDemoRealizationArtifactEntry, ...]


def build_visual_premium_demo_realization_artifact_contract(
) -> VisualPremiumDemoRealizationArtifactContract:
    """Build canonical premium demo realization artifact contract."""
    picture_ready_contract = build_visual_premium_demo_picture_ready_contract()
    picture_ready_entry = picture_ready_contract.entries[0]

    entries = (
        VisualPremiumDemoRealizationArtifactEntry(
            realization_artifact_id="visual_premium_demo_realization_artifact_001",
            picture_ready_id=picture_ready_entry.picture_ready_id,
            realization_artifact_mode="premium_demo_realization_artifact",
            realization_artifact_status="premium_demo_realization_artifact_ready",
            renderer_surface_id=picture_ready_entry.renderer_surface_id,
            theme_id=picture_ready_entry.theme_id,
            screen_id=picture_ready_entry.screen_id,
            preview_artifact_id=picture_ready_entry.preview_artifact_id,
            picture_ready=picture_ready_entry.picture_ready,
            realization_artifact_ready=True,
            truth_bound_realization_artifact=True,
            read_only=True,
            description=(
                "Canonical premium demo realization artifact entry after assembly "
                "of the first truth-preserving premium demo picture-ready layer."
            ),
        ),
    )

    return VisualPremiumDemoRealizationArtifactContract(
        contract_id="visual_premium_demo_realization_artifact_contract_001",
        total_entries=len(entries),
        ready_entries=sum(
            1
            for entry in entries
            if entry.realization_artifact_status
            == "premium_demo_realization_artifact_ready"
        ),
        read_only_entries=sum(1 for entry in entries if entry.read_only),
        entries=entries,
    )

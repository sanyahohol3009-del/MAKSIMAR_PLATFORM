from __future__ import annotations

from dataclasses import dataclass
from typing import Literal

from MAKSIMAR_CORE_LIB.oob_dashboard.visual_premium_demo_realization_artifact_contract import (
    build_visual_premium_demo_realization_artifact_contract,
)


RealizationOutputMode = Literal[
    "premium_demo_realization_output",
]

RealizationOutputStatus = Literal[
    "premium_demo_realization_output_ready",
]


@dataclass(frozen=True, slots=True)
class VisualPremiumDemoRealizationOutputEntry:
    """Canonical premium demo realization output entry."""

    realization_output_id: str
    realization_artifact_id: str
    realization_output_mode: RealizationOutputMode
    realization_output_status: RealizationOutputStatus
    renderer_surface_id: str
    theme_id: str
    screen_id: str
    preview_artifact_id: str
    realization_artifact_ready: bool
    realization_output_ready: bool
    truth_bound_realization_output: bool
    read_only: bool
    description: str


@dataclass(frozen=True, slots=True)
class VisualPremiumDemoRealizationOutputContract:
    """Canonical premium demo realization output contract."""

    contract_id: str
    total_entries: int
    ready_entries: int
    read_only_entries: int
    entries: tuple[VisualPremiumDemoRealizationOutputEntry, ...]


def build_visual_premium_demo_realization_output_contract(
) -> VisualPremiumDemoRealizationOutputContract:
    """Build canonical premium demo realization output contract."""
    realization_artifact_contract = build_visual_premium_demo_realization_artifact_contract()
    realization_artifact_entry = realization_artifact_contract.entries[0]

    entries = (
        VisualPremiumDemoRealizationOutputEntry(
            realization_output_id="visual_premium_demo_realization_output_001",
            realization_artifact_id=realization_artifact_entry.realization_artifact_id,
            realization_output_mode="premium_demo_realization_output",
            realization_output_status="premium_demo_realization_output_ready",
            renderer_surface_id=realization_artifact_entry.renderer_surface_id,
            theme_id=realization_artifact_entry.theme_id,
            screen_id=realization_artifact_entry.screen_id,
            preview_artifact_id=realization_artifact_entry.preview_artifact_id,
            realization_artifact_ready=realization_artifact_entry.realization_artifact_ready,
            realization_output_ready=True,
            truth_bound_realization_output=True,
            read_only=True,
            description=(
                "Canonical premium demo realization output entry after assembly "
                "of the first truth-preserving premium demo realization artifact."
            ),
        ),
    )

    return VisualPremiumDemoRealizationOutputContract(
        contract_id="visual_premium_demo_realization_output_contract_001",
        total_entries=len(entries),
        ready_entries=sum(
            1
            for entry in entries
            if entry.realization_output_status == "premium_demo_realization_output_ready"
        ),
        read_only_entries=sum(1 for entry in entries if entry.read_only),
        entries=entries,
    )

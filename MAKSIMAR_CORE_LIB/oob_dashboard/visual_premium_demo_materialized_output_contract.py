from __future__ import annotations

from dataclasses import dataclass
from typing import Literal

from MAKSIMAR_CORE_LIB.oob_dashboard.visual_premium_demo_realization_output_contract import (
    build_visual_premium_demo_realization_output_contract,
)


MaterializedOutputMode = Literal[
    "premium_demo_materialized_output",
]

MaterializedOutputStatus = Literal[
    "premium_demo_materialized_output_ready",
]


@dataclass(frozen=True, slots=True)
class VisualPremiumDemoMaterializedOutputEntry:
    """Canonical premium demo materialized output entry."""

    materialized_output_id: str
    realization_output_id: str
    materialized_output_mode: MaterializedOutputMode
    materialized_output_status: MaterializedOutputStatus
    renderer_surface_id: str
    theme_id: str
    screen_id: str
    preview_artifact_id: str
    realization_output_ready: bool
    materialized_output_ready: bool
    truth_bound_materialized_output: bool
    read_only: bool
    description: str


@dataclass(frozen=True, slots=True)
class VisualPremiumDemoMaterializedOutputContract:
    """Canonical premium demo materialized output contract."""

    contract_id: str
    total_entries: int
    ready_entries: int
    read_only_entries: int
    entries: tuple[VisualPremiumDemoMaterializedOutputEntry, ...]


def build_visual_premium_demo_materialized_output_contract(
) -> VisualPremiumDemoMaterializedOutputContract:
    """Build canonical premium demo materialized output contract."""
    realization_output_contract = build_visual_premium_demo_realization_output_contract()
    realization_output_entry = realization_output_contract.entries[0]

    entries = (
        VisualPremiumDemoMaterializedOutputEntry(
            materialized_output_id="visual_premium_demo_materialized_output_001",
            realization_output_id=realization_output_entry.realization_output_id,
            materialized_output_mode="premium_demo_materialized_output",
            materialized_output_status="premium_demo_materialized_output_ready",
            renderer_surface_id=realization_output_entry.renderer_surface_id,
            theme_id=realization_output_entry.theme_id,
            screen_id=realization_output_entry.screen_id,
            preview_artifact_id=realization_output_entry.preview_artifact_id,
            realization_output_ready=realization_output_entry.realization_output_ready,
            materialized_output_ready=True,
            truth_bound_materialized_output=True,
            read_only=True,
            description=(
                "Canonical premium demo materialized output entry after assembly "
                "of the first truth-preserving premium demo realization output."
            ),
        ),
    )

    return VisualPremiumDemoMaterializedOutputContract(
        contract_id="visual_premium_demo_materialized_output_contract_001",
        total_entries=len(entries),
        ready_entries=sum(
            1
            for entry in entries
            if entry.materialized_output_status
            == "premium_demo_materialized_output_ready"
        ),
        read_only_entries=sum(1 for entry in entries if entry.read_only),
        entries=entries,
    )

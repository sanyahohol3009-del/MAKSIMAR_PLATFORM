from __future__ import annotations

from dataclasses import dataclass
from typing import Literal

from MAKSIMAR_CORE_LIB.oob_dashboard.visual_premium_demo_realization_bridge_contract import (
    build_visual_premium_demo_realization_bridge_contract,
)


PremiumDemoRealizationReadyMode = Literal[
    "premium_demo_realization_ready",
]

PremiumDemoRealizationReadyStatus = Literal[
    "premium_demo_realization_ready_state",
]


@dataclass(frozen=True, slots=True)
class VisualPremiumDemoRealizationReadyEntry:
    """Canonical premium demo realization-ready entry."""

    realization_ready_id: str
    realization_bridge_id: str
    realization_ready_mode: PremiumDemoRealizationReadyMode
    realization_ready_status: PremiumDemoRealizationReadyStatus
    renderer_surface_id: str
    theme_id: str
    screen_id: str
    preview_artifact_id: str
    realization_bridge_ready: bool
    realization_ready: bool
    truth_bound_realization_ready: bool
    read_only: bool
    description: str


@dataclass(frozen=True, slots=True)
class VisualPremiumDemoRealizationReadyContract:
    """Canonical premium demo realization-ready contract."""

    contract_id: str
    total_entries: int
    ready_entries: int
    read_only_entries: int
    entries: tuple[VisualPremiumDemoRealizationReadyEntry, ...]


def build_visual_premium_demo_realization_ready_contract(
) -> VisualPremiumDemoRealizationReadyContract:
    """Build canonical premium demo realization-ready contract."""
    realization_bridge_contract = build_visual_premium_demo_realization_bridge_contract()
    realization_bridge_entry = realization_bridge_contract.entries[0]

    entries = (
        VisualPremiumDemoRealizationReadyEntry(
            realization_ready_id="visual_premium_demo_realization_ready_001",
            realization_bridge_id=realization_bridge_entry.realization_bridge_id,
            realization_ready_mode="premium_demo_realization_ready",
            realization_ready_status="premium_demo_realization_ready_state",
            renderer_surface_id=realization_bridge_entry.renderer_surface_id,
            theme_id=realization_bridge_entry.theme_id,
            screen_id=realization_bridge_entry.screen_id,
            preview_artifact_id=realization_bridge_entry.preview_artifact_id,
            realization_bridge_ready=realization_bridge_entry.realization_bridge_ready,
            realization_ready=True,
            truth_bound_realization_ready=True,
            read_only=True,
            description=(
                "Canonical premium demo realization-ready entry after assembly "
                "of the first truth-preserving premium demo realization bridge."
            ),
        ),
    )

    return VisualPremiumDemoRealizationReadyContract(
        contract_id="visual_premium_demo_realization_ready_contract_001",
        total_entries=len(entries),
        ready_entries=sum(
            1
            for entry in entries
            if entry.realization_ready_status == "premium_demo_realization_ready_state"
        ),
        read_only_entries=sum(1 for entry in entries if entry.read_only),
        entries=entries,
    )

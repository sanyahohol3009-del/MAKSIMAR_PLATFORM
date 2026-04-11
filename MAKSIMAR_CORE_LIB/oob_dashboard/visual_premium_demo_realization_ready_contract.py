from __future__ import annotations

from dataclasses import dataclass
from typing import Literal


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
    """Build canonical premium demo realization-ready contract.

    This builder is intentionally self-contained to extend the runtime cut
    above the premium demo realization bridge.
    """
    entries = (
        VisualPremiumDemoRealizationReadyEntry(
            realization_ready_id="visual_premium_demo_realization_ready_001",
            realization_bridge_id="visual_premium_demo_realization_bridge_001",
            realization_ready_mode="premium_demo_realization_ready",
            realization_ready_status="premium_demo_realization_ready_state",
            renderer_surface_id="render_surface_workspace_operator_main_001",
            theme_id="visual_theme_operator_hud_001",
            screen_id="visual_hud_screen_001",
            preview_artifact_id="visual_hud_preview_artifact_001",
            realization_bridge_ready=True,
            realization_ready=True,
            truth_bound_realization_ready=True,
            read_only=True,
            description=(
                "Canonical premium demo realization-ready entry as a stable "
                "runtime cut-point above the premium demo realization bridge."
            ),
        ),
    )

    return VisualPremiumDemoRealizationReadyContract(
        contract_id="visual_premium_demo_realization_ready_contract_001",
        total_entries=len(entries),
        ready_entries=sum(
            1
            for entry in entries
            if entry.realization_ready_status
            == "premium_demo_realization_ready_state"
        ),
        read_only_entries=sum(1 for entry in entries if entry.read_only),
        entries=entries,
    )

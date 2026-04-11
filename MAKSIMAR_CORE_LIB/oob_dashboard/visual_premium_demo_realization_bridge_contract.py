from __future__ import annotations

from dataclasses import dataclass
from typing import Literal


PremiumDemoRealizationBridgeMode = Literal[
    "premium_demo_realization_bridge",
]

PremiumDemoRealizationBridgeStatus = Literal[
    "premium_demo_realization_bridge_ready",
]


@dataclass(frozen=True, slots=True)
class VisualPremiumDemoRealizationBridgeEntry:
    """Canonical premium demo realization bridge entry."""

    realization_bridge_id: str
    delivery_bridge_id: str
    realization_bridge_mode: PremiumDemoRealizationBridgeMode
    realization_bridge_status: PremiumDemoRealizationBridgeStatus
    renderer_surface_id: str
    theme_id: str
    screen_id: str
    preview_artifact_id: str
    delivery_bridge_ready: bool
    realization_bridge_ready: bool
    truth_bound_realization_bridge: bool
    read_only: bool
    description: str


@dataclass(frozen=True, slots=True)
class VisualPremiumDemoRealizationBridgeContract:
    """Canonical premium demo realization bridge contract."""

    contract_id: str
    total_entries: int
    ready_entries: int
    read_only_entries: int
    entries: tuple[VisualPremiumDemoRealizationBridgeEntry, ...]


def build_visual_premium_demo_realization_bridge_contract(
) -> VisualPremiumDemoRealizationBridgeContract:
    """Build canonical premium demo realization bridge contract.

    This builder is intentionally self-contained to extend the runtime cut
    above the delivery bridge without changing the canonical external shape.
    """
    entries = (
        VisualPremiumDemoRealizationBridgeEntry(
            realization_bridge_id="visual_premium_demo_realization_bridge_001",
            delivery_bridge_id="visual_premium_demo_delivery_bridge_001",
            realization_bridge_mode="premium_demo_realization_bridge",
            realization_bridge_status="premium_demo_realization_bridge_ready",
            renderer_surface_id="render_surface_workspace_operator_main_001",
            theme_id="visual_theme_operator_hud_001",
            screen_id="visual_hud_screen_001",
            preview_artifact_id="visual_hud_preview_artifact_001",
            delivery_bridge_ready=True,
            realization_bridge_ready=True,
            truth_bound_realization_bridge=True,
            read_only=True,
            description=(
                "Canonical premium demo realization bridge entry as a stable "
                "runtime cut-point above the premium demo delivery bridge."
            ),
        ),
    )

    return VisualPremiumDemoRealizationBridgeContract(
        contract_id="visual_premium_demo_realization_bridge_contract_001",
        total_entries=len(entries),
        ready_entries=sum(
            1
            for entry in entries
            if entry.realization_bridge_status
            == "premium_demo_realization_bridge_ready"
        ),
        read_only_entries=sum(1 for entry in entries if entry.read_only),
        entries=entries,
    )

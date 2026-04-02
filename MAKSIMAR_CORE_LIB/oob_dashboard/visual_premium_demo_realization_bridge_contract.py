from __future__ import annotations

from dataclasses import dataclass
from typing import Literal

from MAKSIMAR_CORE_LIB.oob_dashboard.visual_premium_demo_delivery_bridge_contract import (
    build_visual_premium_demo_delivery_bridge_contract,
)


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
    """Build canonical premium demo realization bridge contract."""
    delivery_bridge_contract = build_visual_premium_demo_delivery_bridge_contract()
    delivery_bridge_entry = delivery_bridge_contract.entries[0]

    entries = (
        VisualPremiumDemoRealizationBridgeEntry(
            realization_bridge_id="visual_premium_demo_realization_bridge_001",
            delivery_bridge_id=delivery_bridge_entry.delivery_bridge_id,
            realization_bridge_mode="premium_demo_realization_bridge",
            realization_bridge_status="premium_demo_realization_bridge_ready",
            renderer_surface_id=delivery_bridge_entry.renderer_surface_id,
            theme_id=delivery_bridge_entry.theme_id,
            screen_id=delivery_bridge_entry.screen_id,
            preview_artifact_id=delivery_bridge_entry.preview_artifact_id,
            delivery_bridge_ready=delivery_bridge_entry.delivery_bridge_ready,
            realization_bridge_ready=True,
            truth_bound_realization_bridge=True,
            read_only=True,
            description=(
                "Canonical premium demo realization bridge entry after assembly "
                "of the first truth-preserving premium demo delivery bridge."
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

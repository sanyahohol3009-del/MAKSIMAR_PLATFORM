from __future__ import annotations

from dataclasses import dataclass
from typing import Literal

from MAKSIMAR_CORE_LIB.oob_dashboard.visual_first_premium_demo_system_contract import (
    build_visual_first_premium_demo_system_contract,
)


PremiumDemoDeliveryBridgeMode = Literal[
    "premium_demo_delivery_bridge",
]

PremiumDemoDeliveryBridgeStatus = Literal[
    "premium_demo_delivery_bridge_ready",
]


@dataclass(frozen=True, slots=True)
class VisualPremiumDemoDeliveryBridgeEntry:
    """Canonical premium demo delivery bridge entry."""

    delivery_bridge_id: str
    premium_demo_system_id: str
    delivery_bridge_mode: PremiumDemoDeliveryBridgeMode
    delivery_bridge_status: PremiumDemoDeliveryBridgeStatus
    renderer_surface_id: str
    theme_id: str
    screen_id: str
    preview_artifact_id: str
    premium_demo_system_ready: bool
    delivery_bridge_ready: bool
    truth_bound_delivery_bridge: bool
    read_only: bool
    description: str


@dataclass(frozen=True, slots=True)
class VisualPremiumDemoDeliveryBridgeContract:
    """Canonical premium demo delivery bridge contract."""

    contract_id: str
    total_entries: int
    ready_entries: int
    read_only_entries: int
    entries: tuple[VisualPremiumDemoDeliveryBridgeEntry, ...]


def build_visual_premium_demo_delivery_bridge_contract(
) -> VisualPremiumDemoDeliveryBridgeContract:
    """Build canonical premium demo delivery bridge contract."""
    premium_demo_system_contract = build_visual_first_premium_demo_system_contract()
    premium_demo_system_entry = premium_demo_system_contract.entries[0]

    entries = (
        VisualPremiumDemoDeliveryBridgeEntry(
            delivery_bridge_id="visual_premium_demo_delivery_bridge_001",
            premium_demo_system_id=premium_demo_system_entry.premium_demo_system_id,
            delivery_bridge_mode="premium_demo_delivery_bridge",
            delivery_bridge_status="premium_demo_delivery_bridge_ready",
            renderer_surface_id=premium_demo_system_entry.renderer_surface_id,
            theme_id=premium_demo_system_entry.theme_id,
            screen_id=premium_demo_system_entry.screen_id,
            preview_artifact_id=premium_demo_system_entry.preview_artifact_id,
            premium_demo_system_ready=premium_demo_system_entry.premium_demo_system_ready,
            delivery_bridge_ready=True,
            truth_bound_delivery_bridge=True,
            read_only=True,
            description=(
                "Canonical premium demo delivery bridge entry after assembly of "
                "the first truth-preserving premium demo system."
            ),
        ),
    )

    return VisualPremiumDemoDeliveryBridgeContract(
        contract_id="visual_premium_demo_delivery_bridge_contract_001",
        total_entries=len(entries),
        ready_entries=sum(
            1
            for entry in entries
            if entry.delivery_bridge_status == "premium_demo_delivery_bridge_ready"
        ),
        read_only_entries=sum(1 for entry in entries if entry.read_only),
        entries=entries,
    )

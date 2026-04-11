from __future__ import annotations

from dataclasses import dataclass
from typing import Literal


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
    """Build canonical premium demo delivery bridge contract.

    This builder is intentionally self-contained to act as a runtime cycle
    cut-point between the premium demo bridge chain and the upper premium/live
    visual chain. The canonical external shape remains unchanged.
    """
    entries = (
        VisualPremiumDemoDeliveryBridgeEntry(
            delivery_bridge_id="visual_premium_demo_delivery_bridge_001",
            premium_demo_system_id="visual_first_premium_demo_system_001",
            delivery_bridge_mode="premium_demo_delivery_bridge",
            delivery_bridge_status="premium_demo_delivery_bridge_ready",
            renderer_surface_id="render_surface_workspace_operator_main_001",
            theme_id="visual_theme_operator_hud_001",
            screen_id="visual_hud_screen_001",
            preview_artifact_id="visual_hud_preview_artifact_001",
            premium_demo_system_ready=True,
            delivery_bridge_ready=True,
            truth_bound_delivery_bridge=True,
            read_only=True,
            description=(
                "Canonical premium demo delivery bridge entry as a stable "
                "runtime cut-point for the premium demo visual bridge chain."
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

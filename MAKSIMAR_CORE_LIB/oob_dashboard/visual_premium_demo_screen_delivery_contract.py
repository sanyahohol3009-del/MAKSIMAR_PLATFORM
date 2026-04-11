from __future__ import annotations

from dataclasses import dataclass
from typing import Literal


PremiumDemoScreenDeliveryMode = Literal[
    "premium_demo_screen_delivery",
]

PremiumDemoScreenDeliveryStatus = Literal[
    "premium_demo_screen_delivery_ready",
]


@dataclass(frozen=True, slots=True)
class VisualPremiumDemoScreenDeliveryEntry:
    """Canonical premium demo screen-delivery entry."""

    screen_delivery_id: str
    realization_ready_id: str
    screen_delivery_mode: PremiumDemoScreenDeliveryMode
    screen_delivery_status: PremiumDemoScreenDeliveryStatus
    renderer_surface_id: str
    theme_id: str
    screen_id: str
    preview_artifact_id: str
    realization_ready: bool
    screen_delivery_ready: bool
    truth_bound_screen_delivery: bool
    read_only: bool
    description: str


@dataclass(frozen=True, slots=True)
class VisualPremiumDemoScreenDeliveryContract:
    """Canonical premium demo screen-delivery contract."""

    contract_id: str
    total_entries: int
    ready_entries: int
    read_only_entries: int
    entries: tuple[VisualPremiumDemoScreenDeliveryEntry, ...]


def build_visual_premium_demo_screen_delivery_contract(
) -> VisualPremiumDemoScreenDeliveryContract:
    """Build canonical premium demo screen-delivery contract.

    This builder is intentionally self-contained to extend the runtime cut
    above the premium demo realization-ready layer.
    """
    entries = (
        VisualPremiumDemoScreenDeliveryEntry(
            screen_delivery_id="visual_premium_demo_screen_delivery_001",
            realization_ready_id="visual_premium_demo_realization_ready_001",
            screen_delivery_mode="premium_demo_screen_delivery",
            screen_delivery_status="premium_demo_screen_delivery_ready",
            renderer_surface_id="render_surface_workspace_operator_main_001",
            theme_id="visual_theme_operator_hud_001",
            screen_id="visual_hud_screen_001",
            preview_artifact_id="visual_hud_preview_artifact_001",
            realization_ready=True,
            screen_delivery_ready=True,
            truth_bound_screen_delivery=True,
            read_only=True,
            description=(
                "Canonical premium demo screen-delivery entry as a stable "
                "runtime cut-point above the premium demo realization-ready layer."
            ),
        ),
    )

    return VisualPremiumDemoScreenDeliveryContract(
        contract_id="visual_premium_demo_screen_delivery_contract_001",
        total_entries=len(entries),
        ready_entries=sum(
            1
            for entry in entries
            if entry.screen_delivery_status == "premium_demo_screen_delivery_ready"
        ),
        read_only_entries=sum(1 for entry in entries if entry.read_only),
        entries=entries,
    )

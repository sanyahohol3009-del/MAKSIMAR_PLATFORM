from __future__ import annotations

from dataclasses import dataclass
from typing import Literal

from MAKSIMAR_CORE_LIB.oob_dashboard.visual_first_viewable_premium_preview_contract import (
    build_visual_first_viewable_premium_preview_contract,
)


PreviewDeliveryReadinessMode = Literal[
    "preview_delivery_readiness",
]

PreviewDeliveryReadinessStatus = Literal[
    "delivery_ready",
]


@dataclass(frozen=True, slots=True)
class VisualPreviewDeliveryReadinessEntry:
    """Canonical preview delivery readiness entry."""

    readiness_id: str
    first_viewable_preview_id: str
    readiness_mode: PreviewDeliveryReadinessMode
    readiness_status: PreviewDeliveryReadinessStatus
    renderer_surface_id: str
    theme_id: str
    screen_id: str
    preview_artifact_id: str
    operator_facing_ready: bool
    delivery_ready: bool
    truth_bound_delivery: bool
    read_only: bool
    description: str


@dataclass(frozen=True, slots=True)
class VisualPreviewDeliveryReadinessContract:
    """Canonical preview delivery readiness contract."""

    contract_id: str
    total_entries: int
    ready_entries: int
    read_only_entries: int
    entries: tuple[VisualPreviewDeliveryReadinessEntry, ...]


def build_visual_preview_delivery_readiness_contract(
) -> VisualPreviewDeliveryReadinessContract:
    """Build canonical preview delivery readiness contract."""
    first_viewable_contract = build_visual_first_viewable_premium_preview_contract()
    first_viewable_entry = first_viewable_contract.entries[0]

    entries = (
        VisualPreviewDeliveryReadinessEntry(
            readiness_id="visual_preview_delivery_readiness_001",
            first_viewable_preview_id=first_viewable_entry.preview_id,
            readiness_mode="preview_delivery_readiness",
            readiness_status="delivery_ready",
            renderer_surface_id=first_viewable_entry.renderer_surface_id,
            theme_id=first_viewable_entry.theme_id,
            screen_id=first_viewable_entry.screen_id,
            preview_artifact_id=first_viewable_entry.preview_artifact_id,
            operator_facing_ready=first_viewable_entry.operator_facing_ready,
            delivery_ready=True,
            truth_bound_delivery=True,
            read_only=True,
            description=(
                "Canonical preview delivery readiness entry after first "
                "viewable premium preview assembly."
            ),
        ),
    )

    return VisualPreviewDeliveryReadinessContract(
        contract_id="visual_preview_delivery_readiness_contract_001",
        total_entries=len(entries),
        ready_entries=sum(
            1 for entry in entries if entry.readiness_status == "delivery_ready"
        ),
        read_only_entries=sum(1 for entry in entries if entry.read_only),
        entries=entries,
    )

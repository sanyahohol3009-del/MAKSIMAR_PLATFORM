from __future__ import annotations

from dataclasses import dataclass
from typing import Literal

from MAKSIMAR_CORE_LIB.oob_dashboard.visual_first_renderer_view_contract import (
    build_visual_first_renderer_view_contract,
)


RendererViewDeliveryMode = Literal[
    "first_renderer_view_delivery",
]

RendererViewDeliveryStatus = Literal[
    "first_renderer_view_delivery_ready",
]


@dataclass(frozen=True, slots=True)
class VisualFirstRendererViewDeliveryEntry:
    """Canonical first renderer-view delivery entry."""

    renderer_view_delivery_id: str
    renderer_view_id: str
    renderer_view_delivery_mode: RendererViewDeliveryMode
    renderer_view_delivery_status: RendererViewDeliveryStatus
    renderer_surface_id: str
    theme_id: str
    screen_id: str
    preview_artifact_id: str
    renderer_view_ready: bool
    renderer_view_delivery_ready: bool
    truth_bound_renderer_view_delivery: bool
    read_only: bool
    description: str


@dataclass(frozen=True, slots=True)
class VisualFirstRendererViewDeliveryContract:
    """Canonical first renderer-view delivery contract."""

    contract_id: str
    total_entries: int
    ready_entries: int
    read_only_entries: int
    entries: tuple[VisualFirstRendererViewDeliveryEntry, ...]


def build_visual_first_renderer_view_delivery_contract(
) -> VisualFirstRendererViewDeliveryContract:
    """Build canonical first renderer-view delivery contract."""
    renderer_view_contract = build_visual_first_renderer_view_contract()
    renderer_view_entry = renderer_view_contract.entries[0]

    entries = (
        VisualFirstRendererViewDeliveryEntry(
            renderer_view_delivery_id="visual_first_renderer_view_delivery_001",
            renderer_view_id=renderer_view_entry.renderer_view_id,
            renderer_view_delivery_mode="first_renderer_view_delivery",
            renderer_view_delivery_status="first_renderer_view_delivery_ready",
            renderer_surface_id=renderer_view_entry.renderer_surface_id,
            theme_id=renderer_view_entry.theme_id,
            screen_id=renderer_view_entry.screen_id,
            preview_artifact_id=renderer_view_entry.preview_artifact_id,
            renderer_view_ready=renderer_view_entry.renderer_view_ready,
            renderer_view_delivery_ready=True,
            truth_bound_renderer_view_delivery=True,
            read_only=True,
            description=(
                "Canonical first renderer-view delivery entry after assembly of "
                "the first truth-preserving renderer view."
            ),
        ),
    )

    return VisualFirstRendererViewDeliveryContract(
        contract_id="visual_first_renderer_view_delivery_contract_001",
        total_entries=len(entries),
        ready_entries=sum(
            1
            for entry in entries
            if entry.renderer_view_delivery_status
            == "first_renderer_view_delivery_ready"
        ),
        read_only_entries=sum(1 for entry in entries if entry.read_only),
        entries=entries,
    )

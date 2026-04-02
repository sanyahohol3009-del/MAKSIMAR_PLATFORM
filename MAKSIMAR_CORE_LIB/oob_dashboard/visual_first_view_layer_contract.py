from __future__ import annotations

from dataclasses import dataclass
from typing import Literal

from MAKSIMAR_CORE_LIB.oob_dashboard.visual_operator_demo_preview_contract import (
    build_visual_operator_demo_preview_contract,
)


ViewLayerMode = Literal[
    "first_view_layer",
]

ViewLayerStatus = Literal[
    "view_layer_ready",
]


@dataclass(frozen=True, slots=True)
class VisualFirstViewLayerEntry:
    """Canonical first view-layer entry."""

    view_layer_id: str
    operator_demo_preview_id: str
    view_layer_mode: ViewLayerMode
    view_layer_status: ViewLayerStatus
    renderer_surface_id: str
    theme_id: str
    screen_id: str
    preview_artifact_id: str
    demo_ready: bool
    view_facing_ready: bool
    truth_bound_view_layer: bool
    read_only: bool
    description: str


@dataclass(frozen=True, slots=True)
class VisualFirstViewLayerContract:
    """Canonical first view-layer contract."""

    contract_id: str
    total_entries: int
    ready_entries: int
    read_only_entries: int
    entries: tuple[VisualFirstViewLayerEntry, ...]


def build_visual_first_view_layer_contract() -> VisualFirstViewLayerContract:
    """Build canonical first view-layer contract."""
    operator_demo_contract = build_visual_operator_demo_preview_contract()
    operator_demo_entry = operator_demo_contract.entries[0]

    entries = (
        VisualFirstViewLayerEntry(
            view_layer_id="visual_first_view_layer_001",
            operator_demo_preview_id=operator_demo_entry.preview_id,
            view_layer_mode="first_view_layer",
            view_layer_status="view_layer_ready",
            renderer_surface_id=operator_demo_entry.renderer_surface_id,
            theme_id=operator_demo_entry.theme_id,
            screen_id=operator_demo_entry.screen_id,
            preview_artifact_id=operator_demo_entry.preview_artifact_id,
            demo_ready=operator_demo_entry.operator_demo_ready,
            view_facing_ready=True,
            truth_bound_view_layer=True,
            read_only=True,
            description=(
                "Canonical first view-layer entry after truth-preserving "
                "operator demo preview assembly."
            ),
        ),
    )

    return VisualFirstViewLayerContract(
        contract_id="visual_first_view_layer_contract_001",
        total_entries=len(entries),
        ready_entries=sum(
            1 for entry in entries if entry.view_layer_status == "view_layer_ready"
        ),
        read_only_entries=sum(1 for entry in entries if entry.read_only),
        entries=entries,
    )

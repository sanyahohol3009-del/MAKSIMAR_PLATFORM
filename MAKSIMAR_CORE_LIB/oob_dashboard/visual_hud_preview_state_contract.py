from __future__ import annotations

from dataclasses import dataclass
from typing import Literal

from MAKSIMAR_CORE_LIB.oob_dashboard.visual_hud_preview_artifact_contract import (
    build_visual_hud_preview_artifact_contract,
)


PreviewStateMode = Literal[
    "operator_hud_preview_state",
]

PreviewStateStatus = Literal[
    "stable",
    "partial",
]


@dataclass(frozen=True, slots=True)
class VisualHudPreviewStateEntry:
    """Canonical HUD preview state entry for first stable whole-screen preview."""

    preview_state_id: str
    artifact_id: str
    renderer_surface_id: str
    theme_id: str
    preview_state_mode: PreviewStateMode
    preview_state_status: PreviewStateStatus
    top_layer_id: str
    center_layer_id: str
    bottom_layer_id: str
    right_sidebar_layer_id: str
    total_layers: int
    visible_layers: int
    read_only: bool
    description: str


@dataclass(frozen=True, slots=True)
class VisualHudPreviewStateContract:
    """Canonical HUD preview state contract for first stable whole-screen preview."""

    contract_id: str
    total_entries: int
    stable_entries: int
    partial_entries: int
    read_only_entries: int
    total_visible_layers: int
    entries: tuple[VisualHudPreviewStateEntry, ...]


def build_visual_hud_preview_state_contract() -> VisualHudPreviewStateContract:
    """Build canonical HUD preview state contract."""
    artifact_contract = build_visual_hud_preview_artifact_contract()
    artifact_entry = artifact_contract.entries[0]

    preview_state_status: PreviewStateStatus = (
        "stable"
        if artifact_entry.artifact_state == "artifact_ready"
        else "partial"
    )

    entries = (
        VisualHudPreviewStateEntry(
            preview_state_id="visual_hud_preview_state_001",
            artifact_id=artifact_entry.artifact_id,
            renderer_surface_id=artifact_entry.renderer_surface_id,
            theme_id=artifact_entry.theme_id,
            preview_state_mode="operator_hud_preview_state",
            preview_state_status=preview_state_status,
            top_layer_id=artifact_entry.top_layer_id,
            center_layer_id=artifact_entry.center_layer_id,
            bottom_layer_id=artifact_entry.bottom_layer_id,
            right_sidebar_layer_id=artifact_entry.right_sidebar_layer_id,
            total_layers=artifact_entry.total_layers,
            visible_layers=artifact_entry.visible_layers,
            read_only=True,
            description=(
                "Canonical HUD preview state entry for first stable preview state."
            ),
        ),
    )

    return VisualHudPreviewStateContract(
        contract_id="visual_hud_preview_state_contract_001",
        total_entries=len(entries),
        stable_entries=sum(
            1 for entry in entries if entry.preview_state_status == "stable"
        ),
        partial_entries=sum(
            1 for entry in entries if entry.preview_state_status == "partial"
        ),
        read_only_entries=sum(1 for entry in entries if entry.read_only),
        total_visible_layers=sum(entry.visible_layers for entry in entries),
        entries=entries,
    )

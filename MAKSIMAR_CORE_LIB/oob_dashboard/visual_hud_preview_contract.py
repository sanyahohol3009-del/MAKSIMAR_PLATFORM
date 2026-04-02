from __future__ import annotations

from dataclasses import dataclass
from typing import Literal

from MAKSIMAR_CORE_LIB.oob_dashboard.visual_hud_snapshot_contract import (
    build_visual_hud_snapshot_contract,
)


PreviewMode = Literal[
    "operator_hud_preview",
]

PreviewState = Literal[
    "ready",
    "previewable",
]


@dataclass(frozen=True, slots=True)
class VisualHudPreviewEntry:
    """Canonical HUD preview entry for first whole-screen preview state."""

    preview_id: str
    snapshot_id: str
    renderer_surface_id: str
    theme_id: str
    preview_mode: PreviewMode
    preview_state: PreviewState
    top_layer_id: str
    center_layer_id: str
    bottom_layer_id: str
    right_sidebar_layer_id: str
    total_layers: int
    visible_layers: int
    read_only: bool
    description: str


@dataclass(frozen=True, slots=True)
class VisualHudPreviewContract:
    """Canonical HUD preview contract for first whole-screen preview state."""

    contract_id: str
    total_entries: int
    ready_entries: int
    previewable_entries: int
    read_only_entries: int
    total_visible_layers: int
    entries: tuple[VisualHudPreviewEntry, ...]


def build_visual_hud_preview_contract() -> VisualHudPreviewContract:
    """Build canonical HUD preview contract."""
    snapshot_contract = build_visual_hud_snapshot_contract()
    snapshot_entry = snapshot_contract.entries[0]

    preview_state: PreviewState = (
        "ready" if snapshot_entry.preview_ready else "previewable"
    )

    entries = (
        VisualHudPreviewEntry(
            preview_id="visual_hud_preview_001",
            snapshot_id=snapshot_entry.snapshot_id,
            renderer_surface_id=snapshot_entry.renderer_surface_id,
            theme_id=snapshot_entry.theme_id,
            preview_mode="operator_hud_preview",
            preview_state=preview_state,
            top_layer_id=snapshot_entry.top_layer_id,
            center_layer_id=snapshot_entry.center_layer_id,
            bottom_layer_id=snapshot_entry.bottom_layer_id,
            right_sidebar_layer_id=snapshot_entry.right_sidebar_layer_id,
            total_layers=snapshot_entry.total_layers,
            visible_layers=snapshot_entry.visible_layers,
            read_only=True,
            description="Canonical HUD preview entry for first preview-ready operator screen.",
        ),
    )

    return VisualHudPreviewContract(
        contract_id="visual_hud_preview_contract_001",
        total_entries=len(entries),
        ready_entries=sum(1 for entry in entries if entry.preview_state == "ready"),
        previewable_entries=sum(
            1 for entry in entries if entry.preview_state == "previewable"
        ),
        read_only_entries=sum(1 for entry in entries if entry.read_only),
        total_visible_layers=sum(entry.visible_layers for entry in entries),
        entries=entries,
    )

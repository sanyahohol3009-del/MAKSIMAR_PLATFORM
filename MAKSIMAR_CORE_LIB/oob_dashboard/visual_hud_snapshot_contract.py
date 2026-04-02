from __future__ import annotations

from dataclasses import dataclass

from MAKSIMAR_CORE_LIB.oob_dashboard.visual_hud_composition_contract import (
    build_visual_hud_composition_contract,
)
from MAKSIMAR_CORE_LIB.oob_dashboard.visual_render_surface_contract import (
    build_visual_render_surface_contract,
)
from MAKSIMAR_CORE_LIB.oob_dashboard.visual_theme_contract import (
    build_visual_theme_contract,
)


@dataclass(frozen=True, slots=True)
class VisualHudSnapshotEntry:
    """Canonical HUD snapshot entry for preview-ready whole-screen state."""

    snapshot_id: str
    renderer_surface_id: str
    theme_id: str
    total_layers: int
    visible_layers: int
    ready_layers: int
    top_layer_id: str
    center_layer_id: str
    bottom_layer_id: str
    right_sidebar_layer_id: str
    read_only: bool
    preview_ready: bool
    description: str


@dataclass(frozen=True, slots=True)
class VisualHudSnapshotContract:
    """Canonical HUD snapshot contract for preview-ready whole-screen state."""

    contract_id: str
    total_entries: int
    preview_ready_entries: int
    read_only_entries: int
    total_visible_layers: int
    total_ready_layers: int
    entries: tuple[VisualHudSnapshotEntry, ...]


def build_visual_hud_snapshot_contract() -> VisualHudSnapshotContract:
    """Build canonical HUD snapshot contract."""
    composition_contract = build_visual_hud_composition_contract()
    render_surface_contract = build_visual_render_surface_contract()
    theme_contract = build_visual_theme_contract()

    renderer_surface_id = render_surface_contract.entries[0].render_surface_id
    theme_id = theme_contract.entries[0].theme_id

    top_layer_id = next(
        entry.hud_layer_id
        for entry in composition_contract.entries
        if entry.layer_role == "top_status_bar"
    )
    center_layer_id = next(
        entry.hud_layer_id
        for entry in composition_contract.entries
        if entry.layer_role == "center_render_surface"
    )
    bottom_layer_id = next(
        entry.hud_layer_id
        for entry in composition_contract.entries
        if entry.layer_role == "bottom_ticker"
    )
    right_sidebar_layer_id = next(
        entry.hud_layer_id
        for entry in composition_contract.entries
        if entry.layer_role == "right_explainability_sidebar"
    )

    visible_layers = sum(1 for entry in composition_contract.entries if entry.visible)
    ready_layers = sum(
        1 for entry in composition_contract.entries if entry.layer_state == "ready"
    )

    entries = (
        VisualHudSnapshotEntry(
            snapshot_id="visual_hud_snapshot_001",
            renderer_surface_id=renderer_surface_id,
            theme_id=theme_id,
            total_layers=composition_contract.total_entries,
            visible_layers=visible_layers,
            ready_layers=ready_layers,
            top_layer_id=top_layer_id,
            center_layer_id=center_layer_id,
            bottom_layer_id=bottom_layer_id,
            right_sidebar_layer_id=right_sidebar_layer_id,
            read_only=True,
            preview_ready=(
                composition_contract.total_entries > 0
                and visible_layers == composition_contract.total_entries
                and ready_layers == composition_contract.total_entries
            ),
            description="Canonical HUD snapshot entry for first preview-ready screen.",
        ),
    )

    return VisualHudSnapshotContract(
        contract_id="visual_hud_snapshot_contract_001",
        total_entries=len(entries),
        preview_ready_entries=sum(1 for entry in entries if entry.preview_ready),
        read_only_entries=sum(1 for entry in entries if entry.read_only),
        total_visible_layers=sum(entry.visible_layers for entry in entries),
        total_ready_layers=sum(entry.ready_layers for entry in entries),
        entries=entries,
    )

from __future__ import annotations

from dataclasses import dataclass
from typing import Literal

from MAKSIMAR_CORE_LIB.oob_dashboard.visual_hud_screen_contract import (
    build_visual_hud_screen_contract,
)


RenderResultState = Literal[
    "composed",
    "render_complete",
]

RenderOutputMode = Literal[
    "operator_hud_render",
]


@dataclass(frozen=True, slots=True)
class VisualHudRenderResultEntry:
    """Canonical HUD render result entry for first render-ready output state."""

    render_result_id: str
    screen_id: str
    renderer_surface_id: str
    theme_id: str
    output_mode: RenderOutputMode
    render_state: RenderResultState
    top_layer_id: str
    center_layer_id: str
    bottom_layer_id: str
    right_sidebar_layer_id: str
    total_layers: int
    visible_layers: int
    read_only: bool
    description: str


@dataclass(frozen=True, slots=True)
class VisualHudRenderResultContract:
    """Canonical HUD render result contract for first render-ready output state."""

    contract_id: str
    total_entries: int
    composed_entries: int
    render_complete_entries: int
    read_only_entries: int
    total_visible_layers: int
    entries: tuple[VisualHudRenderResultEntry, ...]


def build_visual_hud_render_result_contract() -> VisualHudRenderResultContract:
    """Build canonical HUD render result contract."""
    screen_contract = build_visual_hud_screen_contract()
    screen_entry = screen_contract.entries[0]

    render_state: RenderResultState = (
        "render_complete"
        if screen_entry.screen_state == "render_ready"
        else "composed"
    )

    entries = (
        VisualHudRenderResultEntry(
            render_result_id="visual_hud_render_result_001",
            screen_id=screen_entry.screen_id,
            renderer_surface_id=screen_entry.renderer_surface_id,
            theme_id=screen_entry.theme_id,
            output_mode="operator_hud_render",
            render_state=render_state,
            top_layer_id=screen_entry.top_layer_id,
            center_layer_id=screen_entry.center_layer_id,
            bottom_layer_id=screen_entry.bottom_layer_id,
            right_sidebar_layer_id=screen_entry.right_sidebar_layer_id,
            total_layers=screen_entry.total_layers,
            visible_layers=screen_entry.visible_layers,
            read_only=True,
            description=(
                "Canonical HUD render result entry for first whole-screen render output."
            ),
        ),
    )

    return VisualHudRenderResultContract(
        contract_id="visual_hud_render_result_contract_001",
        total_entries=len(entries),
        composed_entries=sum(
            1 for entry in entries if entry.render_state == "composed"
        ),
        render_complete_entries=sum(
            1 for entry in entries if entry.render_state == "render_complete"
        ),
        read_only_entries=sum(1 for entry in entries if entry.read_only),
        total_visible_layers=sum(entry.visible_layers for entry in entries),
        entries=entries,
    )

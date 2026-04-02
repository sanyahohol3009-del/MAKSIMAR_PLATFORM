from __future__ import annotations

from dataclasses import dataclass
from typing import Literal

from MAKSIMAR_CORE_LIB.oob_dashboard.visual_hud_preview_contract import (
    build_visual_hud_preview_contract,
)


ScreenMode = Literal[
    "operator_hud_screen",
]

ScreenState = Literal[
    "ready",
    "render_ready",
]


@dataclass(frozen=True, slots=True)
class VisualHudScreenEntry:
    """Canonical HUD screen entry for first whole-screen visual screen."""

    screen_id: str
    preview_id: str
    renderer_surface_id: str
    theme_id: str
    screen_mode: ScreenMode
    screen_state: ScreenState
    top_layer_id: str
    center_layer_id: str
    bottom_layer_id: str
    right_sidebar_layer_id: str
    total_layers: int
    visible_layers: int
    read_only: bool
    description: str


@dataclass(frozen=True, slots=True)
class VisualHudScreenContract:
    """Canonical HUD screen contract for first whole-screen visual screen."""

    contract_id: str
    total_entries: int
    ready_entries: int
    render_ready_entries: int
    read_only_entries: int
    total_visible_layers: int
    entries: tuple[VisualHudScreenEntry, ...]


def build_visual_hud_screen_contract() -> VisualHudScreenContract:
    """Build canonical HUD screen contract."""
    preview_contract = build_visual_hud_preview_contract()
    preview_entry = preview_contract.entries[0]

    screen_state: ScreenState = (
        "render_ready" if preview_entry.preview_state == "ready" else "ready"
    )

    entries = (
        VisualHudScreenEntry(
            screen_id="visual_hud_screen_001",
            preview_id=preview_entry.preview_id,
            renderer_surface_id=preview_entry.renderer_surface_id,
            theme_id=preview_entry.theme_id,
            screen_mode="operator_hud_screen",
            screen_state=screen_state,
            top_layer_id=preview_entry.top_layer_id,
            center_layer_id=preview_entry.center_layer_id,
            bottom_layer_id=preview_entry.bottom_layer_id,
            right_sidebar_layer_id=preview_entry.right_sidebar_layer_id,
            total_layers=preview_entry.total_layers,
            visible_layers=preview_entry.visible_layers,
            read_only=True,
            description=(
                "Canonical HUD screen entry for first whole-screen visual surface."
            ),
        ),
    )

    return VisualHudScreenContract(
        contract_id="visual_hud_screen_contract_001",
        total_entries=len(entries),
        ready_entries=sum(1 for entry in entries if entry.screen_state == "ready"),
        render_ready_entries=sum(
            1 for entry in entries if entry.screen_state == "render_ready"
        ),
        read_only_entries=sum(1 for entry in entries if entry.read_only),
        total_visible_layers=sum(entry.visible_layers for entry in entries),
        entries=entries,
    )

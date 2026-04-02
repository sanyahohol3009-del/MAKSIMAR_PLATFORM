from __future__ import annotations

from dataclasses import dataclass
from typing import Literal

from MAKSIMAR_CORE_LIB.oob_dashboard.visual_bottom_ticker_contract import (
    build_visual_bottom_ticker_contract,
)
from MAKSIMAR_CORE_LIB.oob_dashboard.visual_explainability_sidebar_contract import (
    build_visual_explainability_sidebar_contract,
)
from MAKSIMAR_CORE_LIB.oob_dashboard.visual_render_surface_contract import (
    build_visual_render_surface_contract,
)
from MAKSIMAR_CORE_LIB.oob_dashboard.visual_signal_overlay_contract import (
    build_visual_signal_overlay_contract,
)
from MAKSIMAR_CORE_LIB.oob_dashboard.visual_status_bar_contract import (
    build_visual_status_bar_contract,
)
from MAKSIMAR_CORE_LIB.oob_dashboard.visual_theme_contract import (
    build_visual_theme_contract,
)
from MAKSIMAR_CORE_LIB.oob_dashboard.visual_topology_overlay_contract import (
    build_visual_topology_overlay_contract,
)


HudLayerRole = Literal[
    "top_status_bar",
    "bottom_ticker",
    "center_render_surface",
    "signal_overlay",
    "topology_overlay",
    "right_explainability_sidebar",
]

HudLayerState = Literal[
    "ready",
    "stacked",
]


@dataclass(frozen=True, slots=True)
class VisualHudCompositionEntry:
    """Canonical visual HUD composition entry."""

    hud_layer_id: str
    layer_role: HudLayerRole
    renderer_surface_id: str
    theme_id: str
    layer_state: HudLayerState
    visible: bool
    read_only: bool
    z_index: int
    description: str


@dataclass(frozen=True, slots=True)
class VisualHudCompositionContract:
    """Canonical visual HUD composition contract."""

    contract_id: str
    total_entries: int
    ready_entries: int
    visible_entries: int
    read_only_entries: int
    max_z_index: int
    entries: tuple[VisualHudCompositionEntry, ...]


def build_visual_hud_composition_contract() -> VisualHudCompositionContract:
    """Build canonical visual HUD composition contract."""
    render_surface_contract = build_visual_render_surface_contract()
    signal_overlay_contract = build_visual_signal_overlay_contract()
    topology_overlay_contract = build_visual_topology_overlay_contract()
    explainability_sidebar_contract = build_visual_explainability_sidebar_contract()
    status_bar_contract = build_visual_status_bar_contract()
    bottom_ticker_contract = build_visual_bottom_ticker_contract()
    theme_contract = build_visual_theme_contract()

    renderer_surface_id = render_surface_contract.entries[0].render_surface_id
    theme_id = theme_contract.entries[0].theme_id

    entries = (
        VisualHudCompositionEntry(
            hud_layer_id="hud_layer_top_status_bar_001",
            layer_role="top_status_bar",
            renderer_surface_id=renderer_surface_id,
            theme_id=theme_id,
            layer_state="ready" if status_bar_contract.total_entries > 0 else "stacked",
            visible=status_bar_contract.visible_entries > 0,
            read_only=True,
            z_index=100,
            description="Canonical top status bar HUD layer.",
        ),
        VisualHudCompositionEntry(
            hud_layer_id="hud_layer_bottom_ticker_001",
            layer_role="bottom_ticker",
            renderer_surface_id=renderer_surface_id,
            theme_id=theme_id,
            layer_state=(
                "ready" if bottom_ticker_contract.total_entries > 0 else "stacked"
            ),
            visible=bottom_ticker_contract.visible_entries > 0,
            read_only=True,
            z_index=90,
            description="Canonical bottom ticker HUD layer.",
        ),
        VisualHudCompositionEntry(
            hud_layer_id="hud_layer_center_render_surface_001",
            layer_role="center_render_surface",
            renderer_surface_id=renderer_surface_id,
            theme_id=theme_id,
            layer_state="ready" if render_surface_contract.total_entries > 0 else "stacked",
            visible=render_surface_contract.total_entries > 0,
            read_only=True,
            z_index=50,
            description="Canonical center render surface HUD layer.",
        ),
        VisualHudCompositionEntry(
            hud_layer_id="hud_layer_signal_overlay_001",
            layer_role="signal_overlay",
            renderer_surface_id=renderer_surface_id,
            theme_id=theme_id,
            layer_state=(
                "ready" if signal_overlay_contract.total_entries > 0 else "stacked"
            ),
            visible=signal_overlay_contract.total_entries > 0,
            read_only=True,
            z_index=70,
            description="Canonical signal overlay HUD layer.",
        ),
        VisualHudCompositionEntry(
            hud_layer_id="hud_layer_topology_overlay_001",
            layer_role="topology_overlay",
            renderer_surface_id=renderer_surface_id,
            theme_id=theme_id,
            layer_state=(
                "ready" if topology_overlay_contract.total_entries > 0 else "stacked"
            ),
            visible=topology_overlay_contract.total_entries > 0,
            read_only=True,
            z_index=60,
            description="Canonical topology overlay HUD layer.",
        ),
        VisualHudCompositionEntry(
            hud_layer_id="hud_layer_right_explainability_sidebar_001",
            layer_role="right_explainability_sidebar",
            renderer_surface_id=renderer_surface_id,
            theme_id=theme_id,
            layer_state=(
                "ready"
                if explainability_sidebar_contract.total_entries > 0
                else "stacked"
            ),
            visible=explainability_sidebar_contract.visible_entries > 0,
            read_only=True,
            z_index=80,
            description="Canonical right explainability sidebar HUD layer.",
        ),
    )

    return VisualHudCompositionContract(
        contract_id="visual_hud_composition_contract_001",
        total_entries=len(entries),
        ready_entries=sum(1 for entry in entries if entry.layer_state == "ready"),
        visible_entries=sum(1 for entry in entries if entry.visible),
        read_only_entries=sum(1 for entry in entries if entry.read_only),
        max_z_index=max(entry.z_index for entry in entries),
        entries=entries,
    )

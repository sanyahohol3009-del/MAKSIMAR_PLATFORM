from __future__ import annotations

from dataclasses import dataclass

from MAKSIMAR_CORE_LIB.oob_dashboard.visual_renderer_contract import (
    build_visual_renderer_contract,
)


@dataclass(frozen=True, slots=True)
class VisualThemeEntry:
    """Canonical visual theme entry."""

    theme_id: str
    renderer_id: str
    theme_name: str
    base_theme_mode: str
    background_style: str
    panel_surface_style: str
    depth_profile: str
    border_style: str
    glow_style: str
    typography_profile: str
    spacing_density: str
    primary_accent: str
    secondary_accent: str
    success_semantic: str
    warning_semantic: str
    critical_semantic: str
    central_core_emphasis: str
    signal_flow_visualization: str
    topology_visualization: str
    explainability_column_style: str
    navigation_column_style: str
    bottom_status_bar_style: str
    degraded_fallback_theme: str
    renderer_ready: bool
    description: str


@dataclass(frozen=True, slots=True)
class VisualThemeContract:
    """Canonical visual theme contract."""

    contract_id: str
    total_entries: int
    renderer_ready_entries: int
    dark_theme_entries: int
    signal_flow_visualization_entries: int
    topology_visualization_entries: int
    entries: tuple[VisualThemeEntry, ...]


def build_visual_theme_contract() -> VisualThemeContract:
    """Build canonical visual theme contract."""
    renderer_contract = build_visual_renderer_contract()

    entries = tuple(
        VisualThemeEntry(
            theme_id="visual_theme_operator_hud_001",
            renderer_id=renderer_entry.renderer_id,
            theme_name="MAKSIMAR Premium Operator HUD",
            base_theme_mode="dark_premium_hud",
            background_style="deep_dark_gradient",
            panel_surface_style="glass_layered_surface",
            depth_profile="deep_multilayer_glass",
            border_style="thin_luminous_frame",
            glow_style="controlled_cyan_amber_glow",
            typography_profile="technical_operator_hierarchy",
            spacing_density="dense_but_readable",
            primary_accent="cyan_blue",
            secondary_accent="amber_orange",
            success_semantic="green_stable_ok",
            warning_semantic="amber_attention",
            critical_semantic="red_failure_only",
            central_core_emphasis="glowing_signal_core",
            signal_flow_visualization="orbital_signal_paths",
            topology_visualization="structured_topology_overlay",
            explainability_column_style="right_explainable_stack",
            navigation_column_style="left_vertical_nav_stack",
            bottom_status_bar_style="persistent_status_ribbon",
            degraded_fallback_theme="minimal_safe_hud",
            renderer_ready=renderer_entry.renderer_ready,
            description=(
                f"Canonical visual theme entry bound to "
                f"{renderer_entry.renderer_id}."
            ),
        )
        for renderer_entry in renderer_contract.entries
    )

    return VisualThemeContract(
        contract_id="visual_theme_contract_001",
        total_entries=len(entries),
        renderer_ready_entries=sum(1 for entry in entries if entry.renderer_ready),
        dark_theme_entries=sum(
            1 for entry in entries if entry.base_theme_mode == "dark_premium_hud"
        ),
        signal_flow_visualization_entries=sum(
            1 for entry in entries if entry.signal_flow_visualization
        ),
        topology_visualization_entries=sum(
            1 for entry in entries if entry.topology_visualization
        ),
        entries=entries,
    )

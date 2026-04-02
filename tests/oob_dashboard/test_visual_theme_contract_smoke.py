from __future__ import annotations

from MAKSIMAR_CORE_LIB.oob_dashboard import (
    build_visual_theme_contract,
)


def test_visual_theme_contract_builds() -> None:
    """Visual theme contract should build successfully."""
    contract = build_visual_theme_contract()

    assert contract.contract_id == "visual_theme_contract_001"
    assert contract.total_entries > 0
    assert contract.renderer_ready_entries == contract.total_entries
    assert contract.dark_theme_entries == contract.total_entries
    assert contract.signal_flow_visualization_entries == contract.total_entries
    assert contract.topology_visualization_entries == contract.total_entries


def test_visual_theme_contract_contains_expected_entry() -> None:
    """Visual theme contract should contain canonical theme entry."""
    contract = build_visual_theme_contract()
    entry = contract.entries[0]

    assert entry.theme_id == "visual_theme_operator_hud_001"
    assert entry.renderer_id == "visual_renderer_001"
    assert entry.theme_name == "MAKSIMAR Premium Operator HUD"
    assert entry.base_theme_mode == "dark_premium_hud"
    assert entry.background_style == "deep_dark_gradient"
    assert entry.panel_surface_style == "glass_layered_surface"
    assert entry.depth_profile == "deep_multilayer_glass"
    assert entry.renderer_ready is True


def test_visual_theme_contract_preserves_color_and_semantic_rules() -> None:
    """Visual theme contract should preserve accent and semantic rules."""
    contract = build_visual_theme_contract()
    entry = contract.entries[0]

    assert entry.primary_accent == "cyan_blue"
    assert entry.secondary_accent == "amber_orange"
    assert entry.success_semantic == "green_stable_ok"
    assert entry.warning_semantic == "amber_attention"
    assert entry.critical_semantic == "red_failure_only"
    assert entry.degraded_fallback_theme == "minimal_safe_hud"


def test_visual_theme_contract_preserves_layout_style_rules() -> None:
    """Visual theme contract should preserve layout style rules."""
    contract = build_visual_theme_contract()
    entry = contract.entries[0]

    assert entry.central_core_emphasis == "glowing_signal_core"
    assert entry.signal_flow_visualization == "orbital_signal_paths"
    assert entry.topology_visualization == "structured_topology_overlay"
    assert entry.explainability_column_style == "right_explainable_stack"
    assert entry.navigation_column_style == "left_vertical_nav_stack"
    assert entry.bottom_status_bar_style == "persistent_status_ribbon"

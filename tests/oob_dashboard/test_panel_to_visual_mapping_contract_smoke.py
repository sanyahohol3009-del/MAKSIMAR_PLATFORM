from __future__ import annotations

from MAKSIMAR_CORE_LIB.oob_dashboard import (
    build_panel_to_visual_mapping_contract,
)


def test_panel_to_visual_mapping_contract_builds() -> None:
    """Panel-to-visual mapping contract should build successfully."""
    contract = build_panel_to_visual_mapping_contract()

    assert contract.contract_id == "panel_to_visual_mapping_contract_001"
    assert contract.total_entries > 0
    assert contract.signal_overlay_entries > 0
    assert contract.topology_overlay_entries > 0
    assert contract.explainability_entries > 0
    assert contract.read_only_entries > 0


def test_panel_to_visual_mapping_contains_foundation_runtime_entry() -> None:
    """Panel-to-visual mapping should contain runtime foundation entry."""
    contract = build_panel_to_visual_mapping_contract()
    entry = next(
        item
        for item in contract.entries
        if item.panel_id == "panel_foundation_runtime_status_001"
    )

    assert entry.display_title == "Runtime Core"
    assert entry.visual_card_type == "status_core_card"
    assert entry.preferred_zone == "center_core"
    assert entry.visual_priority == "primary"
    assert entry.density_mode == "focus"
    assert entry.icon_slot == "core_status_icon"
    assert entry.signal_overlay_participation is True
    assert entry.topology_overlay_participation is True
    assert entry.explainability_binding is True
    assert entry.interaction_class == "read_only"


def test_panel_to_visual_mapping_contains_navigation_entry() -> None:
    """Panel-to-visual mapping should contain navigation entry."""
    contract = build_panel_to_visual_mapping_contract()
    entry = next(
        item for item in contract.entries if item.panel_id == "panel_navigation"
    )

    assert entry.visual_card_type == "navigation_card"
    assert entry.preferred_zone == "left_navigation"
    assert entry.visual_priority == "supporting"
    assert entry.density_mode == "compact"


def test_panel_to_visual_mapping_binds_theme_and_titles() -> None:
    """Panel-to-visual mapping should bind theme and title slots."""
    contract = build_panel_to_visual_mapping_contract()

    for entry in contract.entries:
        assert entry.theme_id == "visual_theme_operator_hud_001"
        assert entry.title_slot == "panel_title_primary"
        assert entry.display_title != ""

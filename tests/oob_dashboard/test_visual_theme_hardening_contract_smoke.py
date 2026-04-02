from __future__ import annotations

from MAKSIMAR_CORE_LIB.oob_dashboard.visual_theme_hardening_contract import (
    build_visual_theme_hardening_contract,
)


def test_visual_theme_hardening_contract_builds() -> None:
    """Visual theme hardening contract should build successfully."""
    contract = build_visual_theme_hardening_contract()

    assert contract.contract_id == "visual_theme_hardening_contract_001"
    assert contract.total_entries == 1
    assert contract.read_only_entries == 1
    assert contract.static_first_entries == 1


def test_visual_theme_hardening_contains_expected_entry() -> None:
    """Visual theme hardening contract should contain canonical hardening entry."""
    contract = build_visual_theme_hardening_contract()
    entry = contract.entries[0]

    assert entry.hardening_id == "visual_theme_hardening_001"
    assert entry.theme_id == "visual_theme_operator_hud_001"
    assert entry.hardening_mode == "phase_1_theme_hardening"
    assert entry.accent_discipline == "blue_orange_operator_hud"
    assert entry.depth_profile == "deep_glass_hud"
    assert entry.glow_profile == "controlled_core_glow"


def test_visual_theme_hardening_preserves_static_first_policy() -> None:
    """Visual theme hardening contract should preserve static-first motion policy."""
    contract = build_visual_theme_hardening_contract()
    entry = contract.entries[0]

    assert entry.motion_policy == "static_first"
    assert entry.read_only is True


def test_visual_theme_hardening_enables_phase_1_visual_strengthening() -> None:
    """Visual theme hardening contract should enable allowed Phase 1 strengthening."""
    contract = build_visual_theme_hardening_contract()
    entry = contract.entries[0]

    assert entry.stronger_panel_hierarchy is True
    assert entry.stronger_zone_separation is True
    assert entry.stronger_center_core_gravity is True
    assert entry.stronger_sidebar_navigation_clarity is True

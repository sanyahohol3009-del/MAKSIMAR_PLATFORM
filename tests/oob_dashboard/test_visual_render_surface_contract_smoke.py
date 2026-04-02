from __future__ import annotations

from MAKSIMAR_CORE_LIB.oob_dashboard import (
    build_visual_render_surface_contract,
)


def test_visual_render_surface_contract_builds() -> None:
    """Visual render surface contract should build successfully."""
    contract = build_visual_render_surface_contract()

    assert contract.contract_id == "visual_render_surface_contract_001"
    assert contract.total_entries > 0
    assert contract.renderer_ready_entries == contract.total_entries
    assert contract.total_render_panels > 0
    assert contract.total_canonical_render_panels > 0


def test_visual_render_surface_contains_expected_entry() -> None:
    """Visual render surface contract should contain canonical render surface entry."""
    contract = build_visual_render_surface_contract()
    entry = contract.entries[0]

    assert entry.render_surface_id == "render_surface_workspace_operator_main_001"
    assert entry.shell_id == "visual_shell_001"
    assert entry.dashboard_id == "dashboard_main_operator_001"
    assert entry.workspace_id == "workspace_operator_main"
    assert entry.display_target_id == "display_primary_operator"
    assert entry.layout_mode == "hud_grid"
    assert entry.hud_mode == "operator_hud"
    assert entry.renderer_ready is True


def test_visual_render_surface_preserves_interaction_boundary() -> None:
    """Visual render surface contract should preserve interaction boundary."""
    contract = build_visual_render_surface_contract()
    entry = contract.entries[0]

    assert entry.read_only_render_surface is False
    assert entry.interactive_render_surface is True


def test_visual_render_surface_uses_canonical_panel_inventory() -> None:
    """Visual render surface contract should use canonical panel inventory."""
    contract = build_visual_render_surface_contract()
    entry = contract.entries[0]

    assert entry.total_render_panels > 0
    assert entry.canonical_render_panels > 0
    assert entry.canonical_render_panels <= contract.total_canonical_render_panels

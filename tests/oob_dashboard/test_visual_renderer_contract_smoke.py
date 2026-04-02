from __future__ import annotations

from MAKSIMAR_CORE_LIB.oob_dashboard import (
    build_visual_renderer_contract,
)


def test_visual_renderer_contract_builds() -> None:
    """Visual renderer contract should build successfully."""
    contract = build_visual_renderer_contract()

    assert contract.contract_id == "visual_renderer_contract_001"
    assert contract.total_entries > 0
    assert contract.renderer_ready_entries == contract.total_entries
    assert contract.canonical_panel_only_entries == contract.total_entries
    assert contract.signal_flow_overlay_entries == contract.total_entries
    assert contract.topology_overlay_entries == contract.total_entries
    assert contract.stalled_path_visibility_entries == contract.total_entries


def test_visual_renderer_contract_contains_expected_entry() -> None:
    """Visual renderer contract should contain canonical renderer entry."""
    contract = build_visual_renderer_contract()
    entry = contract.entries[0]

    assert entry.renderer_id == "visual_renderer_001"
    assert entry.render_surface_id == "render_surface_workspace_operator_main_001"
    assert entry.shell_id == "visual_shell_001"
    assert entry.dashboard_id == "dashboard_main_operator_001"
    assert entry.workspace_id == "workspace_operator_main"
    assert entry.display_target_id == "display_primary_operator"
    assert entry.primary_visual_mode == "operator_hud"
    assert entry.degraded_visual_fallback == "safe_minimal_overlay"
    assert entry.renderer_ready is True


def test_visual_renderer_contract_exposes_signal_and_topology_overlays() -> None:
    """Visual renderer should expose signal and topology overlays."""
    contract = build_visual_renderer_contract()
    entry = contract.entries[0]

    assert entry.canonical_panel_only is True
    assert entry.signal_flow_overlay_enabled is True
    assert entry.topology_overlay_enabled is True
    assert entry.stalled_path_visibility_enabled is True
    assert "operator_hud" in entry.supported_visual_modes
    assert "topology_overlay" in entry.supported_visual_modes
    assert "degraded_fallback" in entry.supported_visual_modes


def test_visual_renderer_contract_preserves_interaction_boundary() -> None:
    """Visual renderer contract should preserve interaction boundary."""
    contract = build_visual_renderer_contract()
    entry = contract.entries[0]

    assert entry.read_only_render_paths is False
    assert entry.interactive_render_paths is True

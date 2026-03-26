from __future__ import annotations

from MAKSIMAR_CORE_LIB.spatial_anchor_resolution import (
    build_spatial_anchor_resolution_contract,
)


def test_spatial_anchor_resolution_contract_builds() -> None:
    """Spatial anchor resolution contract should build successfully."""
    contract = build_spatial_anchor_resolution_contract()

    assert contract.total_entries == 3
    assert contract.engineering_target_entries == 1
    assert contract.dashboard_target_entries == 1
    assert contract.ar_target_entries == 1
    assert contract.resolved_entries == 3


def test_spatial_anchor_resolution_contract_contains_expected_surface_entry() -> None:
    """Spatial anchor resolution should expose expected surface entry."""
    contract = build_spatial_anchor_resolution_contract()
    entry = contract.entries[0]

    assert entry.resolution_entry_id == "spatialview_surface_map_001"
    assert entry.spatial_anchor_id == "anchor_surface_map_001"
    assert entry.resolved_view_target == "view_surface_map_001"
    assert entry.display_target_role == "engineering_display"
    assert entry.anchor_reference_mode == "surface_locked"


def test_spatial_anchor_resolution_contract_contains_expected_validation_entry() -> None:
    """Spatial anchor resolution should expose expected validation entry."""
    contract = build_spatial_anchor_resolution_contract()
    entry = contract.entries[1]

    assert entry.resolution_entry_id == "spatialview_validation_report_001"
    assert entry.spatial_anchor_id == "anchor_validation_report_001"
    assert entry.resolved_view_target == "view_validation_report_001"
    assert entry.display_target_role == "primary_dashboard_display"
    assert entry.anchor_reference_mode == "dashboard_locked"


def test_spatial_anchor_resolution_contract_contains_expected_optics_entry() -> None:
    """Spatial anchor resolution should expose expected optics entry."""
    contract = build_spatial_anchor_resolution_contract()
    entry = contract.entries[2]

    assert entry.resolution_entry_id == "spatialview_optics_mode_001"
    assert entry.spatial_anchor_id == "anchor_optics_mode_001"
    assert entry.resolved_view_target == "view_optics_mode_001"
    assert entry.display_target_role == "ar_glasses_display"
    assert entry.anchor_reference_mode == "optics_locked"

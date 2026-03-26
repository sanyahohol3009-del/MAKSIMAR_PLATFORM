from __future__ import annotations

from MAKSIMAR_CORE_LIB.physics_dashboard_views import (
    build_physics_dashboard_views_contract,
)


def test_physics_dashboard_views_contract_builds() -> None:
    """Physics dashboard views contract should build successfully."""
    contract = build_physics_dashboard_views_contract()

    assert contract.total_entries == 5
    assert contract.engineering_display_entries == 3
    assert contract.primary_dashboard_entries == 2
    assert contract.export_capable_entries == 1
    assert contract.defined_entries == 5


def test_physics_dashboard_views_contract_contains_expected_surface_panel() -> None:
    """Physics dashboard should expose expected surface panel."""
    contract = build_physics_dashboard_views_contract()
    entry = contract.entries[0]

    assert entry.panel_id == "panel_surface_map_001"
    assert entry.view_kind == "surface_map_view"
    assert entry.display_role == "engineering_display"
    assert entry.linked_surface_entry_id == "surfaceintel_aluminum_engraving_001"
    assert entry.linked_material_id == "material_aluminum_001"
    assert entry.export_capable is False


def test_physics_dashboard_views_contract_contains_expected_material_panel() -> None:
    """Physics dashboard should expose expected material panel."""
    contract = build_physics_dashboard_views_contract()
    entry = contract.entries[1]

    assert entry.panel_id == "panel_material_profile_001"
    assert entry.view_kind == "material_profile_view"
    assert entry.display_role == "engineering_display"
    assert entry.linked_material_id == "material_steel_001"
    assert entry.export_capable is False


def test_physics_dashboard_views_contract_contains_expected_validation_panel() -> None:
    """Physics dashboard should expose expected validation panel."""
    contract = build_physics_dashboard_views_contract()
    entry = contract.entries[2]

    assert entry.panel_id == "panel_validation_report_001"
    assert entry.view_kind == "validation_report_view"
    assert entry.display_role == "primary_dashboard_display"
    assert entry.linked_validation_gate_id == "physgate_engineering_realistic_001"
    assert entry.export_capable is False


def test_physics_dashboard_views_contract_contains_expected_export_panel() -> None:
    """Physics dashboard should expose expected export panel."""
    contract = build_physics_dashboard_views_contract()
    entry = contract.entries[4]

    assert entry.panel_id == "panel_project_export_001"
    assert entry.view_kind == "project_export_view"
    assert entry.display_role == "primary_dashboard_display"
    assert entry.linked_validation_gate_id == "physgate_strict_physics_001"
    assert entry.export_capable is True

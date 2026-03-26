from __future__ import annotations

from MAKSIMAR_CORE_LIB.wrist_psc_display_integration import (
    build_wrist_psc_display_integration_contract,
)


def test_wrist_psc_display_integration_contract_builds() -> None:
    """Wrist PSC display integration contract should build successfully."""
    contract = build_wrist_psc_display_integration_contract()

    assert contract.total_entries == 3
    assert contract.engineering_entries == 1
    assert contract.dashboard_entries == 1
    assert contract.ar_entries == 1
    assert contract.integrated_entries == 3


def test_wrist_psc_display_integration_contract_contains_expected_engineering_entry() -> None:
    """Integration contract should expose expected engineering entry."""
    contract = build_wrist_psc_display_integration_contract()
    entry = contract.entries[0]

    assert entry.integration_mode == "wrist_to_engineering_display"
    assert entry.resolution_entry_id == "spatialview_surface_map_001"
    assert entry.resolved_view_id == "view_surface_map_001"
    assert entry.source_panel_id == "panel_surface_map_001"
    assert entry.display_target_role == "engineering_display"


def test_wrist_psc_display_integration_contract_contains_expected_dashboard_entry() -> None:
    """Integration contract should expose expected dashboard entry."""
    contract = build_wrist_psc_display_integration_contract()
    entry = contract.entries[1]

    assert entry.integration_mode == "wrist_to_dashboard_display"
    assert entry.resolution_entry_id == "spatialview_validation_report_001"
    assert entry.resolved_view_id == "view_validation_report_001"
    assert entry.source_panel_id == "panel_validation_report_001"
    assert entry.display_target_role == "primary_dashboard_display"


def test_wrist_psc_display_integration_contract_contains_expected_ar_entry() -> None:
    """Integration contract should expose expected AR entry."""
    contract = build_wrist_psc_display_integration_contract()
    entry = contract.entries[2]

    assert entry.integration_mode == "wrist_to_ar_display"
    assert entry.resolution_entry_id == "spatialview_optics_mode_001"
    assert entry.resolved_view_id == "view_optics_mode_001"
    assert entry.source_panel_id == "panel_optics_mode_001"
    assert entry.display_target_role == "ar_glasses_display"

from __future__ import annotations

from MAKSIMAR_CORE_LIB.oob_dashboard.project_map_panel_contract import (
    build_project_map_panel_contract,
)


def test_project_map_panel_contract_builds() -> None:
    contract = build_project_map_panel_contract()

    assert contract.panel_id == "panel_project_map"
    assert contract.total_entries == 3
    assert contract.read_only_entries == 3
    assert contract.main_dashboard_visible_entries == 3
    assert contract.oob_visible_entries == 3
    assert contract.operator_visible is True


def test_project_map_panel_contract_contains_expected_modules() -> None:
    contract = build_project_map_panel_contract()

    modules = tuple((entry.module_id, entry.layer_name, entry.criticality) for entry in contract.entries)

    assert modules == (
        ("control_plane", "server_control_plane", "high"),
        ("execution_control", "server_execution_control", "high"),
        ("oob_dashboard", "read_only_ui", "medium"),
    )

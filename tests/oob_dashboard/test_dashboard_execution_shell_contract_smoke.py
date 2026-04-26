from __future__ import annotations

from MAKSIMAR_CORE_LIB.oob_dashboard.dashboard_execution_shell_contract import (
    build_dashboard_execution_panels_shell_contract,
)


def test_dashboard_execution_shell_contract_builds() -> None:
    contract = build_dashboard_execution_panels_shell_contract()

    assert contract.shell_id == "dashboard_execution_panels_shell"
    assert contract.total_panels == 7
    assert contract.operator_visible is True


def test_dashboard_execution_shell_contract_contains_expected_panel_totals() -> None:
    contract = build_dashboard_execution_panels_shell_contract()

    assert contract.total_project_map_entries > 0
    assert contract.total_node_topology_entries == 3
    assert contract.total_degraded_mode_entries > 0
    assert contract.total_data_flow_entries == 5
    assert contract.total_dependency_map_entries == 3
    assert contract.total_queue_load_entries > 0
    assert contract.total_version_control_entries > 0

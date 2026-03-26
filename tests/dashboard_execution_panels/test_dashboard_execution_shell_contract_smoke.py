from __future__ import annotations

from MAKSIMAR_CORE_LIB.oob_dashboard import (
    build_dashboard_execution_panels_shell_contract,
)


def test_dashboard_execution_panels_shell_contract_builds() -> None:
    """Dashboard execution panels shell contract should build successfully."""
    shell = build_dashboard_execution_panels_shell_contract()

    assert shell.shell_id == "dashboard_execution_panels_shell"
    assert shell.total_queue_load_entries == 5
    assert shell.total_node_topology_entries == 3
    assert shell.total_degraded_mode_entries == 4


def test_dashboard_execution_panels_shell_contract_counts_all_panels() -> None:
    """Dashboard execution panels shell contract should expose all panel counts."""
    shell = build_dashboard_execution_panels_shell_contract()

    assert shell.total_project_map_entries == 3
    assert shell.total_data_flow_entries == 5
    assert shell.total_dependency_map_entries == 3
    assert shell.total_version_control_entries == 2

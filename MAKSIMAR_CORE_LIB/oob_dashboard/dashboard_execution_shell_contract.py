from __future__ import annotations

from MAKSIMAR_CORE_LIB.oob_dashboard.dashboard_execution_shell_models import (
    DashboardExecutionPanelsShellContract,
)
from MAKSIMAR_CORE_LIB.oob_dashboard.data_flow_panel_contract import (
    build_data_flow_panel_contract,
)
from MAKSIMAR_CORE_LIB.oob_dashboard.degraded_mode_panel_contract import (
    build_degraded_mode_panel_contract,
)
from MAKSIMAR_CORE_LIB.oob_dashboard.dependency_map_panel_contract import (
    build_dependency_map_panel_contract,
)
from MAKSIMAR_CORE_LIB.oob_dashboard.node_topology_panel_contract import (
    build_node_topology_panel_contract,
)
from MAKSIMAR_CORE_LIB.oob_dashboard.project_map_panel_contract import (
    build_project_map_panel_contract,
)
from MAKSIMAR_CORE_LIB.oob_dashboard.queue_load_panel_contract import (
    build_queue_load_panel_contract,
)
from MAKSIMAR_CORE_LIB.oob_dashboard.version_control_panel_contract import (
    build_version_control_panel_contract,
)


def build_dashboard_execution_panels_shell_contract() -> DashboardExecutionPanelsShellContract:
    """Build final shell contract for execution-aware dashboard panels."""
    queue_load = build_queue_load_panel_contract()
    node_topology = build_node_topology_panel_contract()
    degraded_mode = build_degraded_mode_panel_contract()
    project_map = build_project_map_panel_contract()
    data_flow = build_data_flow_panel_contract()
    dependency_map = build_dependency_map_panel_contract()
    version_control = build_version_control_panel_contract()

    return DashboardExecutionPanelsShellContract(
        shell_id="dashboard_execution_panels_shell",
        total_queue_load_entries=queue_load.total_entries,
        total_node_topology_entries=node_topology.total_entries,
        total_degraded_mode_entries=degraded_mode.total_entries,
        total_project_map_entries=project_map.total_entries,
        total_data_flow_entries=data_flow.total_entries,
        total_dependency_map_entries=dependency_map.total_entries,
        total_version_control_entries=version_control.total_entries,
    )

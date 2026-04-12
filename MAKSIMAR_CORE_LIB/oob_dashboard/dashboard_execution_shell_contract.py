from __future__ import annotations

from dataclasses import dataclass

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


@dataclass(frozen=True)
class DashboardExecutionPanelsShellContract:
    """Canonical dashboard execution-panels shell contract."""

    shell_id: str
    total_panels: int
    total_project_map_entries: int
    total_node_topology_entries: int
    total_degraded_mode_entries: int
    total_data_flow_entries: int
    total_dependency_map_entries: int
    total_queue_load_entries: int
    total_version_control_entries: int
    operator_visible: bool
    description: str


def build_dashboard_execution_panels_shell_contract() -> DashboardExecutionPanelsShellContract:
    """Build canonical execution-panels shell contract."""
    project_map = build_project_map_panel_contract()
    node_topology = build_node_topology_panel_contract()
    degraded_mode = build_degraded_mode_panel_contract()
    data_flow = build_data_flow_panel_contract()
    dependency_map = build_dependency_map_panel_contract()
    queue_load = build_queue_load_panel_contract()
    version_control = build_version_control_panel_contract()

    return DashboardExecutionPanelsShellContract(
        shell_id="dashboard_execution_panels_shell",
        total_panels=7,
        total_project_map_entries=project_map.total_entries,
        total_node_topology_entries=node_topology.total_entries,
        total_degraded_mode_entries=degraded_mode.total_entries,
        total_data_flow_entries=data_flow.total_entries,
        total_dependency_map_entries=dependency_map.total_entries,
        total_queue_load_entries=queue_load.total_entries,
        total_version_control_entries=version_control.total_entries,
        operator_visible=True,
        description="Canonical dashboard execution panels shell contract.",
    )

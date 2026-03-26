from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class DashboardExecutionPanelsShellContract:
    """Final shell contract for execution-aware dashboard panels."""

    shell_id: str
    total_queue_load_entries: int
    total_node_topology_entries: int
    total_degraded_mode_entries: int
    total_project_map_entries: int
    total_data_flow_entries: int
    total_dependency_map_entries: int
    total_version_control_entries: int

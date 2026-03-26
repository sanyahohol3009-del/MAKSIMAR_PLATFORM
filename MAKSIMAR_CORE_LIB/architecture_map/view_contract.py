from __future__ import annotations

from MAKSIMAR_CORE_LIB.architecture_map.view_models import (
    DashboardViewEntry,
    DashboardViewRegistryContract,
)


def build_dashboard_view_registry_contract() -> DashboardViewRegistryContract:
    """Build unified dashboard view registry contract."""

    views = (
        DashboardViewEntry(
            view_id="project_map_view",
            source_contract="module_registry",
            panel_name="Project Map Panel",
            read_only=True,
        ),
        DashboardViewEntry(
            view_id="data_flow_view",
            source_contract="flow_map",
            panel_name="Data Flow Panel",
            read_only=True,
        ),
        DashboardViewEntry(
            view_id="dependency_map_view",
            source_contract="dependency_graph",
            panel_name="Dependency / Cube Map Panel",
            read_only=True,
        ),
    )

    return DashboardViewRegistryContract(
        total_views=len(views),
        views=views,
    )

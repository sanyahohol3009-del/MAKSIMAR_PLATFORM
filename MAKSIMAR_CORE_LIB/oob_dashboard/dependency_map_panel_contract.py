from __future__ import annotations

from MAKSIMAR_CORE_LIB.architecture_map import (
    build_dependency_graph_contract,
)
from MAKSIMAR_CORE_LIB.oob_dashboard.dependency_map_panel_models import (
    DependencyMapPanelContract,
    DependencyMapPanelEntry,
)


def build_dependency_map_panel_contract() -> DependencyMapPanelContract:
    """Build unified read-only dependency map panel contract."""
    dependency_contract = build_dependency_graph_contract()

    entries = tuple(
        DependencyMapPanelEntry(
            upstream_module_id=edge.upstream_module_id,
            downstream_module_id=edge.downstream_module_id,
            critical_path=edge.critical_path,
        )
        for edge in dependency_contract.edges
    )

    return DependencyMapPanelContract(
        panel_id="panel_dependency_map",
        total_entries=len(entries),
        entries=entries,
    )

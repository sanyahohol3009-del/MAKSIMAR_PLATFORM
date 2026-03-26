from __future__ import annotations

from MAKSIMAR_CORE_LIB.architecture_map.dependency_models import (
    DependencyEdge,
    DependencyGraphContract,
)


def build_dependency_graph_contract() -> DependencyGraphContract:
    """Build unified dependency graph contract."""

    edges = (
        DependencyEdge(
            upstream_module_id="control_plane",
            downstream_module_id="execution_control",
            critical_path=True,
        ),
        DependencyEdge(
            upstream_module_id="execution_control",
            downstream_module_id="execution_observability",
            critical_path=True,
        ),
        DependencyEdge(
            upstream_module_id="execution_observability",
            downstream_module_id="oob_dashboard",
            critical_path=False,
        ),
    )

    return DependencyGraphContract(
        total_edges=len(edges),
        edges=edges,
    )

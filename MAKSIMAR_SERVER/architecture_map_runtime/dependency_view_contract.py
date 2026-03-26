from __future__ import annotations

from MAKSIMAR_CORE_LIB.architecture_map import (
    build_dependency_graph_contract,
)
from MAKSIMAR_SERVER.architecture_map_runtime.dependency_view_models import (
    ServerDependencyViewContract,
    ServerDependencyViewEntry,
)


def build_server_dependency_view_contract() -> ServerDependencyViewContract:
    """Build unified server-side dependency view contract."""
    dependency_graph = build_dependency_graph_contract()

    edges = tuple(
        ServerDependencyViewEntry(
            upstream_module_id=edge.upstream_module_id,
            downstream_module_id=edge.downstream_module_id,
            critical_path=edge.critical_path,
            source_contract_bound=True,
        )
        for edge in dependency_graph.edges
    )

    return ServerDependencyViewContract(
        total_edges=len(edges),
        edges=edges,
    )

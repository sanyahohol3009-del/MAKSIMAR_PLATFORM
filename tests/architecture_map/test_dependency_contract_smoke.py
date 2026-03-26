from __future__ import annotations

from MAKSIMAR_CORE_LIB.architecture_map import (
    build_dependency_graph_contract,
)


def test_dependency_graph_contract_builds() -> None:
    """Dependency graph contract should build successfully."""
    contract = build_dependency_graph_contract()

    assert contract.total_edges == 3
    assert len(contract.edges) == 3


def test_dependency_graph_contains_execution_path() -> None:
    """Dependency graph should contain execution control dependency path."""
    contract = build_dependency_graph_contract()

    pairs = {
        (edge.upstream_module_id, edge.downstream_module_id)
        for edge in contract.edges
    }

    assert ("control_plane", "execution_control") in pairs
    assert ("execution_control", "execution_observability") in pairs

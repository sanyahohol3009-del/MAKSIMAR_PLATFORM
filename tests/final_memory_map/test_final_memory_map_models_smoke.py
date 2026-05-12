from __future__ import annotations

from MAKSIMAR_SERVER.DASHBOARD_READ_ONLY_VIEWS.final_memory_map import build_final_memory_graph


def test_final_memory_map_models_smoke() -> None:
    graph = build_final_memory_graph()

    assert graph.map_ready is True
    assert len(graph.nodes) >= 7
    assert len(graph.edges) >= 6
    assert graph.dashboard_read_only is True
    assert graph.canonical_write_allowed is False
    assert graph.runtime_mutation_allowed is False

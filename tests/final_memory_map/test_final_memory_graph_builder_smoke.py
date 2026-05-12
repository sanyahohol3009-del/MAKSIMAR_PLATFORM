from __future__ import annotations

from MAKSIMAR_SERVER.DASHBOARD_READ_ONLY_VIEWS.final_memory_map import build_final_memory_graph


def test_final_memory_graph_builder_smoke() -> None:
    graph = build_final_memory_graph()
    node_ids = {node.node_id for node in graph.nodes}

    assert "memory_self_readability" in node_ids
    assert "memory_drift_detection" in node_ids
    assert "mempalace_read_only_adapter" in node_ids
    assert "final_memory_dashboard" in node_ids

from __future__ import annotations

from typing import Dict, Tuple

from MAKSIMAR_SERVER.DASHBOARD_READ_ONLY_VIEWS.final_memory_map.final_memory_graph_builder import (
    build_final_memory_graph,
)


def build_final_memory_storage_map() -> Dict[str, object]:
    graph = build_final_memory_graph()

    storage_nodes: Tuple[str, ...] = tuple(
        node.node_id
        for node in graph.nodes
        if node.node_kind in {"memory_layer", "backend_adapter", "governance_layer", "evidence_layer"}
    )

    return {
        "storage_map_id": "final_memory_storage_map_001",
        "storage_nodes": storage_nodes,
        "storage_node_count": len(storage_nodes),
        "all_storage_nodes_visible": graph.all_storage_nodes_visible,
        "dashboard_read_only": graph.dashboard_read_only,
        "canonical_write_allowed": graph.canonical_write_allowed,
        "runtime_mutation_allowed": graph.runtime_mutation_allowed,
        "storage_map_ready": len(storage_nodes) >= 6,
    }

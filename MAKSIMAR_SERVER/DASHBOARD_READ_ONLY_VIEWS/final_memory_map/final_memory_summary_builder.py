from __future__ import annotations

from typing import Dict

from MAKSIMAR_SERVER.DASHBOARD_READ_ONLY_VIEWS.final_memory_map.final_memory_graph_builder import (
    build_final_memory_graph,
)
from MAKSIMAR_SERVER.DASHBOARD_READ_ONLY_VIEWS.final_memory_map.final_memory_retrieval_map_builder import (
    build_final_memory_retrieval_map,
)
from MAKSIMAR_SERVER.DASHBOARD_READ_ONLY_VIEWS.final_memory_map.final_memory_storage_map_builder import (
    build_final_memory_storage_map,
)


def build_final_memory_summary() -> Dict[str, object]:
    graph = build_final_memory_graph()
    storage = build_final_memory_storage_map()
    retrieval = build_final_memory_retrieval_map()

    summary_ready = (
        graph.map_ready
        and storage["storage_map_ready"] is True
        and retrieval["retrieval_map_ready"] is True
        and graph.dashboard_read_only is True
        and graph.canonical_write_allowed is False
        and graph.runtime_mutation_allowed is False
    )

    return {
        "summary_id": "final_memory_summary_001",
        "summary_ready": summary_ready,
        "node_count": len(graph.nodes),
        "edge_count": len(graph.edges),
        "storage_node_count": storage["storage_node_count"],
        "retrieval_source_count": retrieval["retrieval_source_count"],
        "all_registered_modules_visible": graph.all_registered_modules_visible,
        "all_storage_nodes_visible": graph.all_storage_nodes_visible,
        "all_retrieval_sources_visible": graph.all_retrieval_sources_visible,
        "dashboard_read_only": graph.dashboard_read_only,
        "canonical_write_allowed": graph.canonical_write_allowed,
        "runtime_mutation_allowed": graph.runtime_mutation_allowed,
    }

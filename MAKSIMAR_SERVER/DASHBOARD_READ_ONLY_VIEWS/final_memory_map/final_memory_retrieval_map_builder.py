from __future__ import annotations

from typing import Dict, Tuple

from MAKSIMAR_SERVER.DASHBOARD_READ_ONLY_VIEWS.final_memory_map.final_memory_graph_builder import (
    build_final_memory_graph,
)


def build_final_memory_retrieval_map() -> Dict[str, object]:
    graph = build_final_memory_graph()

    retrieval_sources: Tuple[str, ...] = tuple(node.node_id for node in graph.nodes if node.node_id != "final_memory_dashboard")

    return {
        "retrieval_map_id": "final_memory_retrieval_map_001",
        "retrieval_sources": retrieval_sources,
        "retrieval_source_count": len(retrieval_sources),
        "allowed_query_modes": ("read_only_preview", "evidence_bound_lookup", "dashboard_explanation"),
        "all_retrieval_sources_visible": graph.all_retrieval_sources_visible,
        "canonical_write_allowed": False,
        "runtime_mutation_allowed": False,
        "retrieval_map_ready": len(retrieval_sources) >= 6,
    }

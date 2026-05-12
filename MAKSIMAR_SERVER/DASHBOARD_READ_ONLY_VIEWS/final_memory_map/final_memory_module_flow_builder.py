from __future__ import annotations

from typing import Dict

from MAKSIMAR_SERVER.DASHBOARD_READ_ONLY_VIEWS.final_memory_map.final_memory_graph_builder import (
    build_final_memory_graph,
)


def build_final_memory_module_flow() -> Dict[str, object]:
    graph = build_final_memory_graph()

    return {
        "module_flow_id": "final_memory_module_flow_001",
        "flow": (
            "registered_memory_layers",
            "storage_map",
            "retrieval_map",
            "backend_adapter_status",
            "drift_candidate_visibility",
            "self_readability_explanation",
            "dashboard_read_only_preview",
            "operator_acceptance",
        ),
        "registered_module_count": len(graph.nodes),
        "edge_count": len(graph.edges),
        "all_registered_modules_visible": graph.all_registered_modules_visible,
        "dashboard_read_only": graph.dashboard_read_only,
        "canonical_write_allowed": graph.canonical_write_allowed,
        "runtime_mutation_allowed": graph.runtime_mutation_allowed,
        "module_flow_ready": graph.map_ready,
    }

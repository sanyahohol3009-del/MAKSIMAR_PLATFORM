from __future__ import annotations

from typing import Dict, Tuple
from pathlib import Path

from MAKSIMAR_SERVER.DASHBOARD_READ_ONLY_VIEWS.final_memory_map.final_memory_graph_builder import (
    build_final_memory_graph,
)


def build_final_memory_storage_map() -> Dict[str, object]:
    graph = build_final_memory_graph()

    component_ids = {component.component_id for component in graph.logical_components}
    storage_nodes: Tuple[str, ...] = tuple(
        node.node_id
        for node in graph.nodes
        if node.node_id not in component_ids and node.node_kind in {"memory_layer", "backend_adapter", "governance_layer", "evidence_layer"}
    )

    # Legacy storage_nodes means graph surfaces, including read-models. Physical
    # stores are counted separately by classification and distinct native path.
    physical = tuple(node for node in graph.nodes
        if node.classification in {"CANONICAL_STORE", "CHILD_BACKEND"} and node.storage_path
        and Path(node.storage_path).is_absolute() and Path(node.storage_path).exists())
    physical_paths = tuple(sorted({node.storage_path for node in physical}))
    return {
        "storage_map_id": "final_memory_storage_map_001",
        "storage_nodes": storage_nodes,
        "storage_node_count": len(storage_nodes),
        "storage_node_count_basis": "logical_graph_surfaces; not physical databases",
        "physical_store_paths": physical_paths,
        "physical_store_count": len(physical_paths),
        "physical_store_nodes": tuple(node.node_id for node in physical),
        "logical_projection_count": sum(node.classification == "READ_MODEL" for node in graph.nodes),
        "all_storage_nodes_visible": graph.all_storage_nodes_visible,
        "inventory_coverage": graph.inventory_coverage,
        "whole_organism_inventory_complete": graph.whole_organism_inventory_complete,
        "dashboard_read_only": graph.dashboard_read_only,
        "canonical_write_allowed": graph.canonical_write_allowed,
        "runtime_mutation_allowed": graph.runtime_mutation_allowed,
        "storage_map_ready": len(storage_nodes) >= 6,
    }

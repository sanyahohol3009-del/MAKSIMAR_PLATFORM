from __future__ import annotations

from typing import Dict

from MAKSIMAR_CORE_LIB.memory_engine.history_ingestion.relation_edge_models import (
    RelationEdge,
)
from MAKSIMAR_CORE_LIB.memory_engine.history_ingestion.relation_id_models import (
    RelationId,
)
from MAKSIMAR_CORE_LIB.memory_engine.history_ingestion.storage_node_builder import (
    build_default_storage_nodes,
)


def build_graph_identity_preview() -> Dict[str, object]:
    storage_nodes = build_default_storage_nodes()
    relation = RelationEdge(
        relation_id=RelationId("REL-0001"),
        from_id=storage_nodes[0].storage_node_id.value,
        to_id=storage_nodes[1].storage_node_id.value,
        relation_type="normalized_into",
        graph_ready=True,
    )

    return {
        "storage_node_count": len(storage_nodes),
        "sample_relation_id": relation.relation_id.value,
        "sample_from_id": relation.from_id,
        "sample_to_id": relation.to_id,
        "graph_ready": relation.graph_ready,
    }

from __future__ import annotations

from typing import Dict

from MAKSIMAR_CORE_LIB.memory_engine.history_binding.history_binding_builders import (
    build_history_binding_projection,
)
from MAKSIMAR_CORE_LIB.memory_engine.history_binding.history_binding_models import (
    HistoryBindingProjection,
)


def build_history_binding_registry_projection(
    projection: HistoryBindingProjection | None = None,
) -> Dict[str, object]:
    """Build a registry-facing read-only projection.

    This does not write to MEMORY_REGISTRY. It only produces a candidate payload.
    """

    selected_projection = projection or build_history_binding_projection()

    return {
        "source_layer": selected_projection.source_layer,
        "memory_id": selected_projection.memory_object.memory_id,
        "memory_type": selected_projection.memory_object.memory_type,
        "truth_level": selected_projection.memory_object.truth_level,
        "status": selected_projection.memory_object.status,
        "storage_node_ids": tuple(
            node.storage_node_id.value for node in selected_projection.storage_nodes
        ),
        "relation_ids": tuple(
            relation.relation_id for relation in selected_projection.relations
        ),
        "registry_ready": selected_projection.registry_ready,
        "readable_by_jarvis": selected_projection.readable_by_jarvis,
    }

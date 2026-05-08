from __future__ import annotations

from typing import Dict

from MAKSIMAR_CORE_LIB.memory_engine.history_binding.history_binding_builders import (
    build_history_binding_projection,
)
from MAKSIMAR_CORE_LIB.memory_engine.history_binding.history_binding_models import (
    HistoryBindingProjection,
)


def build_history_binding_traceability_projection(
    projection: HistoryBindingProjection | None = None,
) -> Dict[str, object]:
    """Build a traceability projection over accepted history_ingestion traceability."""

    selected_projection = projection or build_history_binding_projection()
    traceability = selected_projection.traceability_projection

    return {
        "memory_id": traceability.memory_id,
        "source_ref": traceability.source_ref,
        "affected_files": traceability.affected_files,
        "related_flow_nodes": traceability.related_flow_nodes,
        "timeline_id": traceability.timeline_id,
        "traceability_ready": traceability.traceability_ready,
    }

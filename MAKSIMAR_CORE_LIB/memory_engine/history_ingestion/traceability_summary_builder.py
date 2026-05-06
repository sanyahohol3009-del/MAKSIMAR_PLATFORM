from __future__ import annotations

from typing import Dict

from MAKSIMAR_CORE_LIB.memory_engine.history_ingestion.memory_object_models import (
    MemoryObject,
)
from MAKSIMAR_CORE_LIB.memory_engine.history_ingestion.traceability_models import (
    TraceabilityProjection,
)


def build_traceability_projection(
    memory_object: MemoryObject,
) -> TraceabilityProjection:
    return TraceabilityProjection(
        memory_id=memory_object.memory_id,
        source_ref=memory_object.source.source_ref,
        affected_files=memory_object.affects,
        related_flow_nodes=(
            "HSTORE-RAW-001",
            "HSTORE-NORM-001",
            "HSTORE-REG-001",
        ),
        timeline_id=f"TL-{memory_object.memory_id}",
        traceability_ready=True,
    )


def build_traceability_projection_preview(
    memory_object: MemoryObject,
) -> Dict[str, object]:
    projection = build_traceability_projection(memory_object)
    return {
        "memory_id": projection.memory_id,
        "source_ref": projection.source_ref,
        "affected_files_count": len(projection.affected_files),
        "related_flow_nodes_count": len(projection.related_flow_nodes),
        "timeline_id": projection.timeline_id,
        "traceability_ready": projection.traceability_ready,
    }

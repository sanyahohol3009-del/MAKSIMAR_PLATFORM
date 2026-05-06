from __future__ import annotations

from typing import Dict

from MAKSIMAR_CORE_LIB.memory_engine.history_ingestion.filter_projection_models import (
    FilterProjection,
)
from MAKSIMAR_CORE_LIB.memory_engine.history_ingestion.memory_object_models import (
    MemoryObject,
)


def build_filter_projection(
    memory_object: MemoryObject,
) -> FilterProjection:
    return FilterProjection(
        memory_id=memory_object.memory_id,
        status=memory_object.status,
        truth_level=memory_object.truth_level,
        tags=memory_object.tags,
        project_area=memory_object.project_area,
        filter_ready=True,
    )


def build_filter_projection_preview(
    memory_object: MemoryObject,
) -> Dict[str, object]:
    projection = build_filter_projection(memory_object)
    return {
        "memory_id": projection.memory_id,
        "status": projection.status,
        "truth_level": projection.truth_level,
        "tag_count": len(projection.tags),
        "project_area_count": len(projection.project_area),
        "filter_ready": projection.filter_ready,
    }

from __future__ import annotations

from typing import Dict

from MAKSIMAR_CORE_LIB.memory_engine.history_ingestion.memory_object_models import (
    MemoryObject,
)
from MAKSIMAR_CORE_LIB.memory_engine.history_ingestion.panel_projection_models import (
    PanelProjection,
)


def build_panel_projection(
    memory_object: MemoryObject,
) -> PanelProjection:
    return PanelProjection(
        memory_id=memory_object.memory_id,
        title=memory_object.title,
        status=memory_object.status,
        truth_level=memory_object.truth_level,
        project_area=memory_object.project_area,
        affected_files=memory_object.affects,
        panel_ready=True,
    )


def build_panel_projection_preview(
    memory_object: MemoryObject,
) -> Dict[str, object]:
    projection = build_panel_projection(memory_object)
    return {
        "memory_id": projection.memory_id,
        "title": projection.title,
        "status": projection.status,
        "truth_level": projection.truth_level,
        "project_area_count": len(projection.project_area),
        "affected_files_count": len(projection.affected_files),
        "panel_ready": projection.panel_ready,
    }

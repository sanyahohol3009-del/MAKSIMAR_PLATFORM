from __future__ import annotations

from typing import Dict

from MAKSIMAR_CORE_LIB.memory_engine.history_ingestion.memory_object_models import (
    MemoryObject,
)


def build_memory_object_summary(
    memory_object: MemoryObject,
) -> Dict[str, object]:
    return {
        "memory_id": memory_object.memory_id,
        "title": memory_object.title,
        "one_line_summary": memory_object.one_line_summary,
        "status": memory_object.status,
        "truth_level": memory_object.truth_level,
        "project_area": memory_object.project_area,
        "source_ref": memory_object.source.source_ref,
        "affects": memory_object.affects,
        "next_step_id": memory_object.next_step_id,
        "next_step_summary": memory_object.next_step_summary,
        "tags": memory_object.tags,
    }

from __future__ import annotations

from MAKSIMAR_CORE_LIB.memory_engine.history_ingestion.memory_id_allocator import (
    build_memory_object_id,
)
from MAKSIMAR_CORE_LIB.memory_engine.history_ingestion.memory_object_models import (
    MemoryObject,
    MemorySource,
)
from MAKSIMAR_CORE_LIB.memory_engine.history_ingestion.segmentation_models import (
    ExtractedSegment,
)


def build_history_chat_memory_object(
    segment: ExtractedSegment,
    numeric_id: int,
) -> MemoryObject:
    memory_id = build_memory_object_id("HCHAT", numeric_id)

    return MemoryObject(
        memory_id=memory_id.value,
        memory_type="history_chat_unit",
        title=f"History segment {numeric_id}",
        one_line_summary=segment.text[:160],
        status="validated",
        truth_level="raw_archive_fact",
        project_area=("history_ingestion", "memory"),
        source=MemorySource(
            source_type="history_import",
            source_ref=segment.parent_document_id,
            timestamp_utc="2026-05-05T00:00:00Z",
        ),
        affects=(segment.parent_document_id,),
        next_step_id="HISTORY-NORMALIZATION",
        next_step_summary="Continue normalized history ingestion flow.",
        tags=("history", "chat", segment.source_type),
    )

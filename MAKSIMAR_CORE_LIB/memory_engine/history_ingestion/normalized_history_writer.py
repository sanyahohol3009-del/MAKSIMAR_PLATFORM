from __future__ import annotations

from typing import Dict

from MAKSIMAR_CORE_LIB.memory_engine.history_ingestion.normalized_history_models import (
    NormalizedHistoryRecord,
)


def build_normalized_history_write_payload(
    record: NormalizedHistoryRecord,
) -> Dict[str, object]:
    return {
        "record_id": record.record_id,
        "memory_id": record.memory_object.memory_id,
        "memory_type": record.memory_object.memory_type,
        "title": record.memory_object.title,
        "one_line_summary": record.memory_object.one_line_summary,
        "status": record.memory_object.status,
        "truth_level": record.memory_object.truth_level,
        "project_area": record.memory_object.project_area,
        "source_ref": record.memory_object.source.source_ref,
        "storage_node_id": record.storage_node_id,
        "write_path": record.write_path,
        "readable_by_jarvis": record.readable_by_jarvis,
        "canonical_truth": record.canonical_truth,
    }

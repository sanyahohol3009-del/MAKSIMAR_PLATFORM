from __future__ import annotations

from typing import Dict

from MAKSIMAR_CORE_LIB.memory_engine.history_ingestion.normalized_history_models import (
    NormalizedHistoryRecord,
)


def build_normalized_history_read_payload(
    record: NormalizedHistoryRecord,
) -> Dict[str, object]:
    return {
        "record_id": record.record_id,
        "memory_id": record.memory_object.memory_id,
        "title": record.memory_object.title,
        "readable_by_jarvis": record.readable_by_jarvis,
        "write_path": record.write_path,
    }


def build_normalized_history_roundtrip_preview(
    record: NormalizedHistoryRecord,
) -> Dict[str, object]:
    return {
        "record_id": record.record_id,
        "memory_id": record.memory_object.memory_id,
        "storage_node_id": record.storage_node_id,
        "roundtrip_ready": True,
    }

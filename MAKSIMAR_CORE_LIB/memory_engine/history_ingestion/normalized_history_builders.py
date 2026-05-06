from __future__ import annotations

import hashlib
from typing import Dict

from MAKSIMAR_CORE_LIB.memory_engine.history_ingestion.historical_memory_object_builder import (
    build_history_chat_memory_object,
)
from MAKSIMAR_CORE_LIB.memory_engine.history_ingestion.normalized_history_models import (
    NormalizedHistoryRecord,
)
from MAKSIMAR_CORE_LIB.memory_engine.history_ingestion.normalized_history_validators import (
    validate_normalized_history_write_ready,
)
from MAKSIMAR_CORE_LIB.memory_engine.history_ingestion.segmentation_models import (
    ExtractedSegment,
)


def _record_id(memory_id: str, storage_node_id: str) -> str:
    payload = f"{memory_id}|{storage_node_id}"
    digest = hashlib.sha256(payload.encode("utf-8")).hexdigest()
    return f"HNORM-{digest[:12].upper()}"


def build_normalized_history_record(
    segment: ExtractedSegment,
    numeric_id: int,
) -> NormalizedHistoryRecord:
    memory_object = build_history_chat_memory_object(segment, numeric_id)

    record = NormalizedHistoryRecord(
        record_id=_record_id(memory_object.memory_id, "HSTORE-NORM-001"),
        memory_object=memory_object,
        storage_node_id="HSTORE-NORM-001",
        write_path=f"normalized_history/{memory_object.memory_id}.json",
        readable_by_jarvis=True,
        canonical_truth=False,
        deterministic_output=True,
        parallel_safe_by_design=True,
    )
    validate_normalized_history_write_ready(record)
    return record


def build_normalized_history_preview(
    record: NormalizedHistoryRecord,
) -> Dict[str, object]:
    return {
        "record_id": record.record_id,
        "memory_id": record.memory_object.memory_id,
        "memory_type": record.memory_object.memory_type,
        "storage_node_id": record.storage_node_id,
        "write_path": record.write_path,
        "readable_by_jarvis": record.readable_by_jarvis,
        "canonical_truth": record.canonical_truth,
        "deterministic_output": record.deterministic_output,
        "parallel_safe_by_design": record.parallel_safe_by_design,
    }

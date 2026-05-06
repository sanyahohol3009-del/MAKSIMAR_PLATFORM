from __future__ import annotations

from MAKSIMAR_CORE_LIB.memory_engine.history_ingestion.historical_memory_object_builder import (
    build_history_chat_memory_object,
)
from MAKSIMAR_CORE_LIB.memory_engine.history_ingestion.normalized_history_models import (
    NormalizedHistoryRecord,
)
from MAKSIMAR_CORE_LIB.memory_engine.history_ingestion.segmentation_builders import (
    build_segment,
)


def test_normalized_history_models_smoke() -> None:
    segment = build_segment(
        parent_document_id="HDOC-0001",
        source_type="txt",
        segment_kind="chat_segment",
        ordinal=0,
        text="history segment body",
        boundary_label="double_newline_boundary",
    )
    memory_object = build_history_chat_memory_object(segment, 1)

    record = NormalizedHistoryRecord(
        record_id="HNORM-0001",
        memory_object=memory_object,
        storage_node_id="HSTORE-NORM-001",
        write_path="normalized_history/HCHAT-0001.json",
        readable_by_jarvis=True,
        canonical_truth=False,
        deterministic_output=True,
        parallel_safe_by_design=True,
    )

    assert record.readable_by_jarvis is True
    assert record.canonical_truth is False

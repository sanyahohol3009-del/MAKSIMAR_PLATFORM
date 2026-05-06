from __future__ import annotations

from MAKSIMAR_CORE_LIB.memory_engine.history_ingestion.normalized_history_builders import (
    build_normalized_history_record,
)
from MAKSIMAR_CORE_LIB.memory_engine.history_ingestion.normalized_history_writer import (
    build_normalized_history_write_payload,
)
from MAKSIMAR_CORE_LIB.memory_engine.history_ingestion.segmentation_builders import (
    build_segment,
)


def test_normalized_history_writer_smoke() -> None:
    segment = build_segment(
        parent_document_id="HDOC-0002",
        source_type="md",
        segment_kind="chat_segment",
        ordinal=0,
        text="segment",
        boundary_label="double_newline_boundary",
    )
    record = build_normalized_history_record(segment, 1)
    payload = build_normalized_history_write_payload(record)

    assert payload["memory_id"] == "HCHAT-0001"
    assert payload["storage_node_id"] == "HSTORE-NORM-001"

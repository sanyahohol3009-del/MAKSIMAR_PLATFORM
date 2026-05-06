from __future__ import annotations

from MAKSIMAR_CORE_LIB.memory_engine.history_ingestion.normalized_history_builders import (
    build_normalized_history_record,
)
from MAKSIMAR_CORE_LIB.memory_engine.history_ingestion.normalized_history_reader import (
    build_normalized_history_read_payload,
)
from MAKSIMAR_CORE_LIB.memory_engine.history_ingestion.normalized_history_writer import (
    build_normalized_history_write_payload,
)
from MAKSIMAR_CORE_LIB.memory_engine.history_ingestion.segmentation_builders import (
    build_segment,
)


def test_normalized_history_roundtrip_ready_smoke() -> None:
    segment = build_segment(
        parent_document_id="HDOC-0010",
        source_type="json",
        segment_kind="chat_segment",
        ordinal=0,
        text="segment",
        boundary_label="double_newline_boundary",
    )
    record = build_normalized_history_record(segment, 9)

    write_payload = build_normalized_history_write_payload(record)
    read_payload = build_normalized_history_read_payload(record)

    assert write_payload["record_id"] == read_payload["record_id"]

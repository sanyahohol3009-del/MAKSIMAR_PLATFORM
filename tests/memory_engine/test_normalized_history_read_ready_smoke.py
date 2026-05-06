from __future__ import annotations

from MAKSIMAR_CORE_LIB.memory_engine.history_ingestion.normalized_history_builders import (
    build_normalized_history_record,
)
from MAKSIMAR_CORE_LIB.memory_engine.history_ingestion.normalized_history_validators import (
    validate_normalized_history_read_ready,
)
from MAKSIMAR_CORE_LIB.memory_engine.history_ingestion.segmentation_builders import (
    build_segment,
)


def test_normalized_history_read_ready_smoke() -> None:
    segment = build_segment(
        parent_document_id="HDOC-0008",
        source_type="html",
        segment_kind="chat_segment",
        ordinal=0,
        text="segment",
        boundary_label="double_newline_boundary",
    )
    record = build_normalized_history_record(segment, 7)

    validate_normalized_history_read_ready(record)
    assert record.readable_by_jarvis is True

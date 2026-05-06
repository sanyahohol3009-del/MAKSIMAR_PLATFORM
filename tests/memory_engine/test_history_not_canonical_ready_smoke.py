from __future__ import annotations

from MAKSIMAR_CORE_LIB.memory_engine.history_ingestion.normalized_history_builders import (
    build_normalized_history_record,
)
from MAKSIMAR_CORE_LIB.memory_engine.history_ingestion.segmentation_builders import (
    build_segment,
)


def test_history_not_canonical_ready_smoke() -> None:
    segment = build_segment(
        parent_document_id="HDOC-0011",
        source_type="txt",
        segment_kind="chat_segment",
        ordinal=0,
        text="segment",
        boundary_label="double_newline_boundary",
    )
    record = build_normalized_history_record(segment, 10)

    assert record.canonical_truth is False

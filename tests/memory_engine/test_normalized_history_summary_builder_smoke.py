from __future__ import annotations

from MAKSIMAR_CORE_LIB.memory_engine.history_ingestion.normalized_history_builders import (
    build_normalized_history_record,
)
from MAKSIMAR_CORE_LIB.memory_engine.history_ingestion.normalized_history_summary_builder import (
    build_normalized_history_summary,
)
from MAKSIMAR_CORE_LIB.memory_engine.history_ingestion.segmentation_builders import (
    build_segment,
)


def test_normalized_history_summary_builder_smoke() -> None:
    segment = build_segment(
        parent_document_id="HDOC-0004",
        source_type="txt",
        segment_kind="chat_segment",
        ordinal=0,
        text="segment",
        boundary_label="double_newline_boundary",
    )
    record = build_normalized_history_record(segment, 3)
    summary = build_normalized_history_summary(record)

    assert summary["memory_id"] == "HCHAT-0003"
    assert summary["canonical_truth"] is False

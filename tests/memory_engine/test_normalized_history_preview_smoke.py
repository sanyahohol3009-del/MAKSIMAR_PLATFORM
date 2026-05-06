from __future__ import annotations

from MAKSIMAR_CORE_LIB.memory_engine.history_ingestion.normalized_history_builders import (
    build_normalized_history_preview,
    build_normalized_history_record,
)
from MAKSIMAR_CORE_LIB.memory_engine.history_ingestion.segmentation_builders import (
    build_segment,
)


def test_normalized_history_preview_smoke() -> None:
    segment = build_segment(
        parent_document_id="HDOC-0006",
        source_type="md",
        segment_kind="chat_segment",
        ordinal=0,
        text="segment",
        boundary_label="double_newline_boundary",
    )
    record = build_normalized_history_record(segment, 5)
    preview = build_normalized_history_preview(record)

    assert preview["memory_id"] == "HCHAT-0005"
    assert preview["readable_by_jarvis"] is True

from __future__ import annotations

from MAKSIMAR_CORE_LIB.memory_engine.history_ingestion.normalized_history_builders import (
    build_normalized_history_record,
)
from MAKSIMAR_CORE_LIB.memory_engine.history_ingestion.normalized_history_reader import (
    build_normalized_history_roundtrip_preview,
)
from MAKSIMAR_CORE_LIB.memory_engine.history_ingestion.segmentation_builders import (
    build_segment,
)


def test_normalized_history_roundtrip_preview_smoke() -> None:
    segment = build_segment(
        parent_document_id="HDOC-0007",
        source_type="txt",
        segment_kind="chat_segment",
        ordinal=0,
        text="segment",
        boundary_label="double_newline_boundary",
    )
    record = build_normalized_history_record(segment, 6)
    preview = build_normalized_history_roundtrip_preview(record)

    assert preview["memory_id"] == "HCHAT-0006"
    assert preview["roundtrip_ready"] is True

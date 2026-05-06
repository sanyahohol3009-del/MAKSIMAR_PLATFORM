from __future__ import annotations

from MAKSIMAR_CORE_LIB.memory_engine.history_ingestion.normalized_history_builders import (
    build_normalized_history_record,
)
from MAKSIMAR_CORE_LIB.memory_engine.history_ingestion.normalized_history_validators import (
    validate_normalized_history_write_ready,
)
from MAKSIMAR_CORE_LIB.memory_engine.history_ingestion.segmentation_builders import (
    build_segment,
)


def test_normalized_history_write_ready_smoke() -> None:
    segment = build_segment(
        parent_document_id="HDOC-0009",
        source_type="md",
        segment_kind="chat_segment",
        ordinal=0,
        text="segment",
        boundary_label="double_newline_boundary",
    )
    record = build_normalized_history_record(segment, 8)

    validate_normalized_history_write_ready(record)
    assert record.parallel_safe_by_design is True

from __future__ import annotations

import pytest

from MAKSIMAR_CORE_LIB.memory_engine.history_ingestion.segmentation_models import (
    ExtractedSegment,
)


def test_segmentation_models_smoke() -> None:
    segment = ExtractedSegment(
        segment_id="HSEG-0001",
        parent_document_id="HDOC-0001",
        source_type="html",
        segment_kind="chat_segment",
        ordinal=0,
        text="hello",
        boundary_label="double_newline_boundary",
        stable_boundary=True,
        deterministic_output=True,
        parallel_safe_by_design=True,
    )

    assert segment.segment_kind == "chat_segment"
    assert segment.ordinal == 0


def test_segmentation_models_reject_empty_text() -> None:
    with pytest.raises(ValueError, match="text must be a non-empty string"):
        ExtractedSegment(
            segment_id="HSEG-0002",
            parent_document_id="HDOC-0002",
            source_type="txt",
            segment_kind="document_section",
            ordinal=0,
            text="",
            boundary_label="blank_line_section_boundary",
            stable_boundary=True,
            deterministic_output=True,
            parallel_safe_by_design=True,
        )

from __future__ import annotations

from MAKSIMAR_CORE_LIB.memory_engine.history_ingestion.archive_source_builders import (
    build_file_archive_source,
)
from MAKSIMAR_CORE_LIB.memory_engine.history_ingestion.document_section_segmenter import (
    segment_document_sections,
)
from MAKSIMAR_CORE_LIB.memory_engine.history_ingestion.segmentation_builders import (
    build_segmentation_preview,
)
from MAKSIMAR_CORE_LIB.memory_engine.history_ingestion.unified_extraction_reader import (
    read_unified_extraction,
)


def test_segment_boundary_preview_smoke() -> None:
    source = build_file_archive_source(
        source_type="md",
        source_path="/tmp/history.md",
        text_payload="section1\n\nsection2",
        binary_available=False,
    )
    document = read_unified_extraction(source)
    segments = segment_document_sections(document)
    preview = build_segmentation_preview(segments)

    assert preview["first_boundary_label"] == "blank_line_section_boundary"
    assert preview["last_ordinal"] == 1

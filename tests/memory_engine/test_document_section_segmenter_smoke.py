from __future__ import annotations

from MAKSIMAR_CORE_LIB.memory_engine.history_ingestion.archive_source_builders import (
    build_file_archive_source,
)
from MAKSIMAR_CORE_LIB.memory_engine.history_ingestion.document_section_segmenter import (
    segment_document_sections,
)
from MAKSIMAR_CORE_LIB.memory_engine.history_ingestion.unified_extraction_reader import (
    read_unified_extraction,
)


def test_document_section_segmenter_smoke() -> None:
    source = build_file_archive_source(
        source_type="md",
        source_path="/tmp/history.md",
        text_payload="# A\nline1\n\n# B\nline2",
        binary_available=False,
    )
    document = read_unified_extraction(source)
    segments = segment_document_sections(document)

    assert len(segments) == 2
    assert segments[0].segment_kind == "document_section"
    assert segments[1].ordinal == 1

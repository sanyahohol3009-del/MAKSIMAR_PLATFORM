from __future__ import annotations

from MAKSIMAR_CORE_LIB.memory_engine.history_ingestion.archive_source_builders import (
    build_file_archive_source,
)
from MAKSIMAR_CORE_LIB.memory_engine.history_ingestion.chat_segmenter import (
    segment_chat_document,
)
from MAKSIMAR_CORE_LIB.memory_engine.history_ingestion.unified_extraction_reader import (
    read_unified_extraction,
)


def test_chat_segmenter_smoke() -> None:
    source = build_file_archive_source(
        source_type="txt",
        source_path="/tmp/history.txt",
        text_payload="first block\n\nsecond block",
        binary_available=False,
    )
    document = read_unified_extraction(source)
    segments = segment_chat_document(document)

    assert len(segments) == 2
    assert segments[0].segment_kind == "chat_segment"
    assert segments[0].ordinal == 0
    assert segments[1].ordinal == 1

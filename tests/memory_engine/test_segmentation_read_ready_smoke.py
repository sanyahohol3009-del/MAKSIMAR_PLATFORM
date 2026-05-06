from __future__ import annotations

from MAKSIMAR_CORE_LIB.memory_engine.history_ingestion.archive_source_builders import (
    build_file_archive_source,
)
from MAKSIMAR_CORE_LIB.memory_engine.history_ingestion.chat_segmenter import (
    segment_chat_document,
)
from MAKSIMAR_CORE_LIB.memory_engine.history_ingestion.segmentation_validators import (
    validate_segmentation_read_ready,
)
from MAKSIMAR_CORE_LIB.memory_engine.history_ingestion.unified_extraction_reader import (
    read_unified_extraction,
)


def test_segmentation_read_ready_smoke() -> None:
    source = build_file_archive_source(
        source_type="html",
        source_path="/tmp/history.html",
        text_payload="one\n\ntwo",
        binary_available=False,
    )
    document = read_unified_extraction(source)
    segments = segment_chat_document(document)

    validate_segmentation_read_ready(segments)
    assert len(segments) == 2

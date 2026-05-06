from __future__ import annotations

from MAKSIMAR_CORE_LIB.memory_engine.history_ingestion.archive_source_builders import (
    build_file_archive_source,
)
from MAKSIMAR_CORE_LIB.memory_engine.history_ingestion.chat_segmenter import (
    segment_chat_document,
)
from MAKSIMAR_CORE_LIB.memory_engine.history_ingestion.segmentation_validators import (
    validate_segment_sequence,
)
from MAKSIMAR_CORE_LIB.memory_engine.history_ingestion.unified_extraction_reader import (
    read_unified_extraction,
)


def test_segmentation_order_smoke() -> None:
    source = build_file_archive_source(
        source_type="html",
        source_path="/tmp/history.html",
        text_payload="<p>a</p>\n\n<p>b</p>\n\n<p>c</p>",
        binary_available=False,
    )
    document = read_unified_extraction(source)
    segments = segment_chat_document(document)

    validate_segment_sequence(segments)
    assert [segment.ordinal for segment in segments] == [0, 1, 2]

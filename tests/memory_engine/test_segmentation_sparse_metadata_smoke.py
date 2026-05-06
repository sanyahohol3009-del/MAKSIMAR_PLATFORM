from __future__ import annotations

from MAKSIMAR_CORE_LIB.memory_engine.history_ingestion.archive_source_builders import (
    build_file_archive_source,
)
from MAKSIMAR_CORE_LIB.memory_engine.history_ingestion.message_extractor import (
    extract_message_units,
)
from MAKSIMAR_CORE_LIB.memory_engine.history_ingestion.unified_extraction_reader import (
    read_unified_extraction,
)


def test_segmentation_sparse_metadata_smoke() -> None:
    source = build_file_archive_source(
        source_type="json",
        source_path="/tmp/history.json",
        text_payload='{"messages": ["user: hi", "assistant: hello"]}',
        binary_available=False,
    )
    document = read_unified_extraction(source)
    segments = extract_message_units(document)

    assert len(segments) >= 1

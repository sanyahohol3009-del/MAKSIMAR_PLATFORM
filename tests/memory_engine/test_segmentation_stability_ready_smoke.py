from __future__ import annotations

from MAKSIMAR_CORE_LIB.memory_engine.history_ingestion.archive_source_builders import (
    build_file_archive_source,
)
from MAKSIMAR_CORE_LIB.memory_engine.history_ingestion.message_extractor import (
    extract_message_units,
)
from MAKSIMAR_CORE_LIB.memory_engine.history_ingestion.segmentation_validators import (
    validate_segmentation_read_ready,
)
from MAKSIMAR_CORE_LIB.memory_engine.history_ingestion.unified_extraction_reader import (
    read_unified_extraction,
)


def test_segmentation_stability_ready_smoke() -> None:
    source = build_file_archive_source(
        source_type="txt",
        source_path="/tmp/history.txt",
        text_payload="user: hi\nassistant: hello",
        binary_available=False,
    )
    document = read_unified_extraction(source)
    segments = extract_message_units(document)

    validate_segmentation_read_ready(segments)
    assert all(segment.stable_boundary for segment in segments)
    assert all(segment.deterministic_output for segment in segments)

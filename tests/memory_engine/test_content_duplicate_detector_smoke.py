from __future__ import annotations

from MAKSIMAR_CORE_LIB.memory_engine.history_ingestion.archive_source_builders import (
    build_file_archive_source,
)
from MAKSIMAR_CORE_LIB.memory_engine.history_ingestion.content_duplicate_detector import (
    detect_content_duplicate,
)
from MAKSIMAR_CORE_LIB.memory_engine.history_ingestion.content_fingerprint_builder import (
    build_content_fingerprint,
)
from MAKSIMAR_CORE_LIB.memory_engine.history_ingestion.unified_extraction_reader import (
    read_unified_extraction,
)


def test_content_duplicate_detector_smoke() -> None:
    source = build_file_archive_source(
        source_type="md",
        source_path="/tmp/history.md",
        text_payload="# alpha",
        binary_available=False,
    )
    doc = read_unified_extraction(source)
    content_hash = build_content_fingerprint(doc).sha256_hex

    assert detect_content_duplicate(doc, [content_hash]) is True

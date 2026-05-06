from __future__ import annotations

from MAKSIMAR_CORE_LIB.memory_engine.history_ingestion.archive_source_builders import (
    build_file_archive_source,
)
from MAKSIMAR_CORE_LIB.memory_engine.history_ingestion.unit_duplicate_detector import (
    detect_unit_duplicates,
)
from MAKSIMAR_CORE_LIB.memory_engine.history_ingestion.unit_fingerprint_builder import (
    build_unit_fingerprint,
)
from MAKSIMAR_CORE_LIB.memory_engine.history_ingestion.unified_extraction_reader import (
    read_unified_extraction,
)


def test_unit_duplicate_detector_smoke() -> None:
    source = build_file_archive_source(
        source_type="json",
        source_path="/tmp/history.json",
        text_payload='{"k": "v"}',
        binary_available=False,
    )
    doc = read_unified_extraction(source)
    unit_hash = build_unit_fingerprint(doc.contents[0]).sha256_hex

    duplicate_count, new_count = detect_unit_duplicates(doc.contents, [unit_hash])

    assert duplicate_count == 1
    assert new_count == 0

from __future__ import annotations

from MAKSIMAR_CORE_LIB.memory_engine.history_ingestion.archive_source_builders import (
    build_file_archive_source,
)
from MAKSIMAR_CORE_LIB.memory_engine.history_ingestion.unified_extraction_reader import (
    read_unified_extraction,
)
from MAKSIMAR_CORE_LIB.memory_engine.history_ingestion.unit_fingerprint_builder import (
    build_unit_fingerprint,
)


def test_unit_fingerprint_builder_smoke() -> None:
    source = build_file_archive_source(
        source_type="json",
        source_path="/tmp/history.json",
        text_payload='{"a": 1}',
        binary_available=False,
    )
    document = read_unified_extraction(source)
    fingerprint = build_unit_fingerprint(document.contents[0])

    assert fingerprint.fingerprint_kind == "unit_fingerprint"
    assert fingerprint.unit_id == document.contents[0].content_id
    assert len(fingerprint.sha256_hex) == 64

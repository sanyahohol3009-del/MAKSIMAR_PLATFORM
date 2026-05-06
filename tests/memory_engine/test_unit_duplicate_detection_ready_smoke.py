from __future__ import annotations

from MAKSIMAR_CORE_LIB.memory_engine.history_ingestion.archive_source_builders import (
    build_file_archive_source,
)
from MAKSIMAR_CORE_LIB.memory_engine.history_ingestion.fingerprint_validators import (
    validate_unit_fingerprint_ready,
)
from MAKSIMAR_CORE_LIB.memory_engine.history_ingestion.unified_extraction_reader import (
    read_unified_extraction,
)
from MAKSIMAR_CORE_LIB.memory_engine.history_ingestion.unit_fingerprint_builder import (
    build_unit_fingerprint,
)


def test_unit_duplicate_detection_ready_smoke() -> None:
    source = build_file_archive_source(
        source_type="md",
        source_path="/tmp/history.md",
        text_payload="# same",
        binary_available=False,
    )
    document = read_unified_extraction(source)
    fingerprint = build_unit_fingerprint(document.contents[0])
    validate_unit_fingerprint_ready(fingerprint)

    assert fingerprint.deterministic is True
    assert fingerprint.parallel_safe_by_design is True

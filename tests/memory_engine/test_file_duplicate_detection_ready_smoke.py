from __future__ import annotations

from MAKSIMAR_CORE_LIB.memory_engine.history_ingestion.archive_source_builders import (
    build_file_archive_source,
)
from MAKSIMAR_CORE_LIB.memory_engine.history_ingestion.file_fingerprint_builder import (
    build_file_fingerprint,
)
from MAKSIMAR_CORE_LIB.memory_engine.history_ingestion.fingerprint_validators import (
    validate_file_fingerprint_ready,
)


def test_file_duplicate_detection_ready_smoke() -> None:
    source = build_file_archive_source(
        source_type="pdf",
        source_path="/tmp/history.pdf",
        text_payload=None,
        binary_available=True,
    )
    fingerprint = build_file_fingerprint(source)
    validate_file_fingerprint_ready(fingerprint)

    assert fingerprint.deterministic is True
    assert fingerprint.parallel_safe_by_design is True

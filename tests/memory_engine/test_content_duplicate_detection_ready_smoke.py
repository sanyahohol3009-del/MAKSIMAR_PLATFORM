from __future__ import annotations

from MAKSIMAR_CORE_LIB.memory_engine.history_ingestion.archive_source_builders import (
    build_file_archive_source,
)
from MAKSIMAR_CORE_LIB.memory_engine.history_ingestion.content_fingerprint_builder import (
    build_content_fingerprint,
)
from MAKSIMAR_CORE_LIB.memory_engine.history_ingestion.fingerprint_validators import (
    validate_content_fingerprint_ready,
)
from MAKSIMAR_CORE_LIB.memory_engine.history_ingestion.unified_extraction_reader import (
    read_unified_extraction,
)


def test_content_duplicate_detection_ready_smoke() -> None:
    source = build_file_archive_source(
        source_type="html",
        source_path="/tmp/history.html",
        text_payload="<html>same</html>",
        binary_available=False,
    )
    document = read_unified_extraction(source)
    fingerprint = build_content_fingerprint(document)
    validate_content_fingerprint_ready(fingerprint)

    assert fingerprint.deterministic is True
    assert fingerprint.parallel_safe_by_design is True

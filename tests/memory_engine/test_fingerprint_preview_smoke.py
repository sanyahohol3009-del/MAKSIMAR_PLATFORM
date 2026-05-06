from __future__ import annotations

from MAKSIMAR_CORE_LIB.memory_engine.history_ingestion.archive_source_builders import (
    build_file_archive_source,
)
from MAKSIMAR_CORE_LIB.memory_engine.history_ingestion.fingerprint_registry_builder import (
    build_fingerprint_preview,
)


def test_fingerprint_preview_smoke() -> None:
    source = build_file_archive_source(
        source_type="txt",
        source_path="/tmp/history.txt",
        text_payload="history",
        binary_available=False,
    )

    preview = build_fingerprint_preview(source)

    assert preview["file_fingerprint_count"] == 1
    assert preview["content_fingerprint_count"] == 1
    assert preview["unit_fingerprint_count"] == 1
    assert preview["file_duplicate_detection_ready"] is True

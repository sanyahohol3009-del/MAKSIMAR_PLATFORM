from __future__ import annotations

from MAKSIMAR_CORE_LIB.memory_engine.history_ingestion.archive_source_builders import (
    build_file_archive_source,
)
from MAKSIMAR_CORE_LIB.memory_engine.history_ingestion.fingerprint_registry_builder import (
    build_fingerprint_registry_for_source,
)


def test_fingerprint_registry_smoke() -> None:
    source = build_file_archive_source(
        source_type="html",
        source_path="/tmp/history.html",
        text_payload="<html>history</html>",
        binary_available=False,
    )

    registry = build_fingerprint_registry_for_source(source)

    assert len(registry.file_fingerprints) == 1
    assert len(registry.content_fingerprints) == 1
    assert len(registry.unit_fingerprints) == 1
    assert registry.file_duplicate_detection_ready is True
    assert registry.content_duplicate_detection_ready is True
    assert registry.unit_duplicate_detection_ready is True

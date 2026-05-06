from __future__ import annotations

from MAKSIMAR_CORE_LIB.memory_engine.history_ingestion.archive_source_builders import (
    build_archive_source_readiness_snapshot,
    build_file_archive_source,
)


def test_archive_source_read_ready_smoke() -> None:
    source = build_file_archive_source(
        source_type="json",
        source_path="/tmp/history.json",
        text_payload='{"history": true}',
        binary_available=False,
    )

    readiness = build_archive_source_readiness_snapshot(source)

    assert readiness["source_type"] == "json"
    assert readiness["read_ready"] is True
    assert readiness["supports_direct_text_read"] is True
    assert readiness["binary_available"] is False

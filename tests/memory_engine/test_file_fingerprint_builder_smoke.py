from __future__ import annotations

from MAKSIMAR_CORE_LIB.memory_engine.history_ingestion.archive_source_builders import (
    build_file_archive_source,
)
from MAKSIMAR_CORE_LIB.memory_engine.history_ingestion.file_fingerprint_builder import (
    build_file_fingerprint,
)


def test_file_fingerprint_builder_smoke() -> None:
    source = build_file_archive_source(
        source_type="txt",
        source_path="/tmp/history.txt",
        text_payload="history",
        binary_available=False,
    )

    fingerprint = build_file_fingerprint(source)

    assert fingerprint.fingerprint_kind == "file_fingerprint"
    assert fingerprint.source_id == source.metadata.source_id
    assert len(fingerprint.sha256_hex) == 64
    assert fingerprint.deterministic is True
    assert fingerprint.parallel_safe_by_design is True

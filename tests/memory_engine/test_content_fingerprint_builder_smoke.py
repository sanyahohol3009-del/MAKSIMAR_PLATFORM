from __future__ import annotations

from MAKSIMAR_CORE_LIB.memory_engine.history_ingestion.archive_source_builders import (
    build_file_archive_source,
)
from MAKSIMAR_CORE_LIB.memory_engine.history_ingestion.content_fingerprint_builder import (
    build_content_fingerprint,
)
from MAKSIMAR_CORE_LIB.memory_engine.history_ingestion.unified_extraction_reader import (
    read_unified_extraction,
)


def test_content_fingerprint_builder_smoke() -> None:
    source = build_file_archive_source(
        source_type="md",
        source_path="/tmp/history.md",
        text_payload="# history",
        binary_available=False,
    )
    document = read_unified_extraction(source)
    fingerprint = build_content_fingerprint(document)

    assert fingerprint.fingerprint_kind == "content_fingerprint"
    assert fingerprint.document_id == document.document_id
    assert len(fingerprint.sha256_hex) == 64

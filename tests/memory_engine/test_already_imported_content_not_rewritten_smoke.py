from __future__ import annotations

from MAKSIMAR_CORE_LIB.memory_engine.history_ingestion.archive_source_builders import (
    build_file_archive_source,
)
from MAKSIMAR_CORE_LIB.memory_engine.history_ingestion.content_fingerprint_builder import (
    build_content_fingerprint,
)
from MAKSIMAR_CORE_LIB.memory_engine.history_ingestion.incremental_import_resolver import (
    resolve_incremental_import,
)
from MAKSIMAR_CORE_LIB.memory_engine.history_ingestion.unified_extraction_reader import (
    read_unified_extraction,
)


def test_already_imported_content_not_rewritten_smoke() -> None:
    source = build_file_archive_source(
        source_type="md",
        source_path="/tmp/history.md",
        text_payload="# same",
        binary_available=False,
    )
    doc = read_unified_extraction(source)
    content_hash = build_content_fingerprint(doc).sha256_hex

    decision = resolve_incremental_import(
        source=source,
        existing_file_hashes=[],
        existing_content_hashes=[content_hash],
        existing_unit_hashes=[],
    )

    assert decision.content_already_imported is True

from __future__ import annotations

from MAKSIMAR_CORE_LIB.memory_engine.history_ingestion.archive_source_builders import (
    build_file_archive_source,
)
from MAKSIMAR_CORE_LIB.memory_engine.history_ingestion.incremental_import_resolver import (
    resolve_incremental_import,
)
from MAKSIMAR_CORE_LIB.memory_engine.history_ingestion.unit_fingerprint_builder import (
    build_unit_fingerprint,
)
from MAKSIMAR_CORE_LIB.memory_engine.history_ingestion.unified_extraction_reader import (
    read_unified_extraction,
)


def test_partial_new_content_resolution_smoke() -> None:
    source_existing = build_file_archive_source(
        source_type="txt",
        source_path="/tmp/old.txt",
        text_payload="same",
        binary_available=False,
    )
    existing_doc = read_unified_extraction(source_existing)
    existing_unit_hash = build_unit_fingerprint(existing_doc.contents[0]).sha256_hex

    source_new = build_file_archive_source(
        source_type="txt",
        source_path="/tmp/new.txt",
        text_payload="different",
        binary_available=False,
    )

    decision = resolve_incremental_import(
        source=source_new,
        existing_file_hashes=[],
        existing_content_hashes=[],
        existing_unit_hashes=[existing_unit_hash],
    )

    assert decision.new_unit_count == 1
    assert decision.write_required is True

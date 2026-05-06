from __future__ import annotations

from MAKSIMAR_CORE_LIB.memory_engine.history_ingestion.archive_source_builders import (
    build_file_archive_source,
)
from MAKSIMAR_CORE_LIB.memory_engine.history_ingestion.file_fingerprint_builder import (
    build_file_fingerprint,
)
from MAKSIMAR_CORE_LIB.memory_engine.history_ingestion.incremental_import_resolver import (
    resolve_incremental_import,
)


def test_already_imported_file_not_rewritten_smoke() -> None:
    source = build_file_archive_source(
        source_type="txt",
        source_path="/tmp/history.txt",
        text_payload="same",
        binary_available=False,
    )
    file_hash = build_file_fingerprint(source).sha256_hex

    decision = resolve_incremental_import(
        source=source,
        existing_file_hashes=[file_hash],
        existing_content_hashes=[],
        existing_unit_hashes=[],
    )

    assert decision.file_already_imported is True
    assert decision.write_required is False

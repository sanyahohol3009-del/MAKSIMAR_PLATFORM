from __future__ import annotations

from MAKSIMAR_CORE_LIB.memory_engine.history_ingestion.archive_source_builders import (
    build_file_archive_source,
)
from MAKSIMAR_CORE_LIB.memory_engine.history_ingestion.incremental_import_resolver import (
    resolve_incremental_import,
)


def test_incremental_import_resolver_smoke() -> None:
    source = build_file_archive_source(
        source_type="txt",
        source_path="/tmp/history.txt",
        text_payload="new content",
        binary_available=False,
    )

    decision = resolve_incremental_import(
        source=source,
        existing_file_hashes=[],
        existing_content_hashes=[],
        existing_unit_hashes=[],
    )

    assert decision.write_required is True
    assert decision.new_unit_count == 1

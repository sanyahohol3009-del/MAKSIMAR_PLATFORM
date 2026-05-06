from __future__ import annotations

from MAKSIMAR_CORE_LIB.memory_engine.history_ingestion.archive_source_builders import (
    build_file_archive_source,
)
from MAKSIMAR_CORE_LIB.memory_engine.history_ingestion.dedup_builders import (
    build_incremental_import_preview,
)


def test_incremental_import_preview_smoke() -> None:
    source = build_file_archive_source(
        source_type="html",
        source_path="/tmp/history.html",
        text_payload="<p>alpha</p>",
        binary_available=False,
    )
    preview = build_incremental_import_preview(
        source=source,
        existing_file_hashes=[],
        existing_content_hashes=[],
        existing_unit_hashes=[],
    )

    assert preview["incremental_import_ready"] is True
    assert preview["new_unit_count"] == 1

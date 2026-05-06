from __future__ import annotations

from MAKSIMAR_CORE_LIB.memory_engine.history_ingestion.archive_source_builders import (
    build_file_archive_source,
)
from MAKSIMAR_CORE_LIB.memory_engine.history_ingestion.incremental_import_resolver import (
    resolve_incremental_import,
)


def test_duplicate_detection_ready_smoke() -> None:
    source = build_file_archive_source(
        source_type="json",
        source_path="/tmp/history.json",
        text_payload='{"alpha": true}',
        binary_available=False,
    )

    decision = resolve_incremental_import(
        source=source,
        existing_file_hashes=[],
        existing_content_hashes=[],
        existing_unit_hashes=[],
    )

    assert decision.deterministic_output is True
    assert decision.parallel_safe_by_design is True

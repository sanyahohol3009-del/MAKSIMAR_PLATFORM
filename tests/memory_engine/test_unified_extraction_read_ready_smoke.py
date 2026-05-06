from __future__ import annotations

from MAKSIMAR_CORE_LIB.memory_engine.history_ingestion.archive_source_builders import (
    build_file_archive_source,
)
from MAKSIMAR_CORE_LIB.memory_engine.history_ingestion.unified_extraction_reader import (
    read_unified_extraction,
)


def test_unified_extraction_read_ready_smoke() -> None:
    source = build_file_archive_source(
        source_type="json",
        source_path="/tmp/history.json",
        text_payload='{"ok": true}',
        binary_available=False,
    )

    document = read_unified_extraction(source)

    assert document.source_type == "json"
    assert document.has_structured_text is True
    assert document.deterministic_output is True
    assert document.parallel_safe_by_design is True

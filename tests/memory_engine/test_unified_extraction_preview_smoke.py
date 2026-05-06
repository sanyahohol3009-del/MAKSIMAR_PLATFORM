from __future__ import annotations

from MAKSIMAR_CORE_LIB.memory_engine.history_ingestion.archive_source_builders import (
    build_file_archive_source,
)
from MAKSIMAR_CORE_LIB.memory_engine.history_ingestion.extraction_builders import (
    build_unified_extraction_preview,
)


def test_unified_extraction_preview_smoke() -> None:
    source = build_file_archive_source(
        source_type="md",
        source_path="/tmp/history.md",
        text_payload="# history",
        binary_available=False,
    )

    preview = build_unified_extraction_preview(source)

    assert preview["source_type"] == "md"
    assert preview["content_count"] == 1
    assert preview["has_structured_text"] is True
    assert preview["extraction_path"] == "direct_text_read"

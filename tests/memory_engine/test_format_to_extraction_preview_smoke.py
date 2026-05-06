from __future__ import annotations

from MAKSIMAR_CORE_LIB.memory_engine.history_ingestion.archive_source_builders import (
    build_file_archive_source,
)
from MAKSIMAR_CORE_LIB.memory_engine.history_ingestion.extraction_builders import (
    build_unified_extraction_preview,
)


def test_format_to_extraction_preview_smoke() -> None:
    source = build_file_archive_source(
        source_type="pdf",
        source_path="/tmp/history.pdf",
        text_payload=None,
        binary_available=True,
    )

    preview = build_unified_extraction_preview(source)

    assert preview["source_type"] == "pdf"
    assert preview["has_structured_text"] is False
    assert preview["extraction_path"] == "binary_reference_capture"
    assert preview["parallel_safe_by_design"] is True

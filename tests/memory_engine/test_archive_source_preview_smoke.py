from __future__ import annotations

from MAKSIMAR_CORE_LIB.memory_engine.history_ingestion.archive_source_builders import (
    build_archive_source_preview,
    build_file_archive_source,
)


def test_archive_source_preview_smoke() -> None:
    source = build_file_archive_source(
        source_type="md",
        source_path="/tmp/history.md",
        text_payload="# history",
        binary_available=False,
    )

    preview = build_archive_source_preview(source)

    assert preview["source_type"] == "md"
    assert preview["source_name"] == "history.md"
    assert preview["supports_direct_text_read"] is True
    assert preview["is_text_first_source"] is True
    assert preview["previewable"] is True

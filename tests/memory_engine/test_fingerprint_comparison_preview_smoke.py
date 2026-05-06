from __future__ import annotations

from MAKSIMAR_CORE_LIB.memory_engine.history_ingestion.archive_source_builders import (
    build_file_archive_source,
)
from MAKSIMAR_CORE_LIB.memory_engine.history_ingestion.fingerprint_registry_builder import (
    build_fingerprint_comparison_preview,
)


def test_fingerprint_comparison_preview_smoke() -> None:
    left = build_file_archive_source(
        source_type="txt",
        source_path="/tmp/a.txt",
        text_payload="same content",
        binary_available=False,
    )
    right = build_file_archive_source(
        source_type="txt",
        source_path="/tmp/b.txt",
        text_payload="same content",
        binary_available=False,
    )

    preview = build_fingerprint_comparison_preview(left, right)

    assert preview["same_file_fingerprint"] is False
    assert preview["same_content_fingerprint"] is True
    assert preview["same_unit_fingerprint"] is True

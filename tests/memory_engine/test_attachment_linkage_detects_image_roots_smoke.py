from __future__ import annotations

from MAKSIMAR_CORE_LIB.memory_engine.history_ingestion.attachment_linkage_builder import (
    build_attachment_linkage_result,
)


def test_attachment_linkage_detects_image_roots_smoke() -> None:
    result = build_attachment_linkage_result(
        "runtime_imports/chatgpt_export_01",
    )
    assert result.image_attachment_root_count == 1

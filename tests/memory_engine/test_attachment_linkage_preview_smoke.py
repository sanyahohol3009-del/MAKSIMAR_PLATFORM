from __future__ import annotations

from MAKSIMAR_CORE_LIB.memory_engine.history_ingestion.attachment_linkage_builder import (
    build_attachment_linkage_preview,
)


def test_attachment_linkage_preview_smoke() -> None:
    preview = build_attachment_linkage_preview(
        "runtime_imports/chatgpt_export_01",
    )
    assert preview["attachment_linkage_ready"] is True

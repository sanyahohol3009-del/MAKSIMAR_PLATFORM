from __future__ import annotations

from MAKSIMAR_CORE_LIB.memory_engine.history_ingestion.message_attachment_linkage_summary_builder import (
    build_message_attachment_linkage_summary,
)


def test_message_attachment_linkage_summary_builder_smoke() -> None:
    summary = build_message_attachment_linkage_summary(
        "runtime_imports/chatgpt_export_01",
    )
    assert summary["message_attachment_linkage_ready"] is True

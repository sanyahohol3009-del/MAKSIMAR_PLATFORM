from __future__ import annotations

from MAKSIMAR_CORE_LIB.memory_engine.history_ingestion.message_attachment_linkage_builder import (
    build_message_attachment_linkage_preview,
)


def test_message_attachment_linkage_conversation_scope_smoke() -> None:
    preview = build_message_attachment_linkage_preview(
        "runtime_imports/chatgpt_export_01",
    )
    assert preview["linkage_scope_kind"] == "message_candidate_preparation"

from __future__ import annotations

from MAKSIMAR_CORE_LIB.memory_engine.history_ingestion.live_import_conversation_reader import (
    build_live_import_conversation_preview,
)


def test_live_import_conversation_preview_smoke() -> None:
    preview = build_live_import_conversation_preview(
        "runtime_imports/chatgpt_export_01/conversations.json",
    )
    assert preview["conversation_count"] >= 1

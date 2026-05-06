from __future__ import annotations

from MAKSIMAR_CORE_LIB.memory_engine.history_ingestion.live_import_conversation_reader import (
    read_live_import_conversations,
)


def test_live_import_conversation_reader_smoke() -> None:
    conversations = read_live_import_conversations(
        "runtime_imports/chatgpt_export_01/conversations.json",
    )
    assert len(conversations) >= 1

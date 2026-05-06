from __future__ import annotations

from MAKSIMAR_CORE_LIB.memory_engine.history_ingestion.live_import_conversation_models import (
    LiveImportConversation,
)


def test_live_import_conversation_models_smoke() -> None:
    model = LiveImportConversation(
        conversation_id="conv-1",
        source_file_path="/tmp/conversations.json",
        message_count=2,
        message_node_ids=("node-1", "node-2"),
        primary_bucket_path="normalized_history/conversations/conv-1",
        live_import_ready=True,
    )
    assert model.live_import_ready is True

from __future__ import annotations

from typing import Dict, Tuple

from MAKSIMAR_CORE_LIB.memory_engine.history_ingestion.live_import_conversation_models import (
    LiveImportConversation,
)
from MAKSIMAR_CORE_LIB.memory_engine.history_ingestion.live_import_conversation_reader import (
    read_live_import_conversations,
)


def build_live_import_conversation_buckets(
    conversations_json_path: str,
) -> Tuple[Dict[str, object], ...]:
    conversations = read_live_import_conversations(conversations_json_path)
    buckets = []
    for conversation in conversations:
        buckets.append(
            {
                "conversation_id": conversation.conversation_id,
                "bucket_path": conversation.primary_bucket_path,
                "message_count": conversation.message_count,
                "message_node_ids": conversation.message_node_ids,
                "bucket_ready": True,
            }
        )
    return tuple(buckets)


def build_live_import_bucket_preview(
    conversations_json_path: str,
) -> Dict[str, object]:
    buckets = build_live_import_conversation_buckets(conversations_json_path)
    first = buckets[0]
    return {
        "bucket_count": len(buckets),
        "first_conversation_id": first["conversation_id"],
        "first_bucket_path": first["bucket_path"],
        "first_message_count": first["message_count"],
        "bucket_ready": first["bucket_ready"],
    }

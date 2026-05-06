from __future__ import annotations

import json
from pathlib import Path
from typing import Dict, List, Tuple

from MAKSIMAR_CORE_LIB.memory_engine.history_ingestion.live_import_conversation_models import (
    LiveImportConversation,
)


def _extract_message_node_ids(mapping: object) -> Tuple[str, ...]:
    if not isinstance(mapping, dict):
        raise ValueError("mapping must be a dict")

    message_node_ids: List[str] = []
    for node_id, node_payload in mapping.items():
        if not isinstance(node_id, str) or not node_id.strip():
            continue
        if not isinstance(node_payload, dict):
            continue
        message_payload = node_payload.get("message")
        if message_payload is not None:
            message_node_ids.append(node_id)

    if not message_node_ids:
        raise ValueError("No message nodes found in conversation mapping")

    return tuple(message_node_ids)


def read_live_import_conversations(
    conversations_json_path: str,
) -> Tuple[LiveImportConversation, ...]:
    source_path = Path(conversations_json_path)
    raw = json.loads(source_path.read_text(encoding="utf-8"))

    if not isinstance(raw, list):
        raise ValueError("conversations.json root must be a list")

    conversations: List[LiveImportConversation] = []
    for item in raw:
        if not isinstance(item, dict):
            continue

        conversation_id = item.get("conversation_id") or item.get("id")
        if not isinstance(conversation_id, str) or not conversation_id.strip():
            continue

        mapping = item.get("mapping")
        message_node_ids = _extract_message_node_ids(mapping)

        conversations.append(
            LiveImportConversation(
                conversation_id=conversation_id,
                source_file_path=str(source_path),
                message_count=len(message_node_ids),
                message_node_ids=message_node_ids,
                primary_bucket_path=(
                    f"normalized_history/conversations/{conversation_id}"
                ),
                live_import_ready=True,
            )
        )

    if not conversations:
        raise ValueError("No conversations parsed from conversations.json")

    return tuple(conversations)


def build_live_import_conversation_preview(
    conversations_json_path: str,
) -> Dict[str, object]:
    conversations = read_live_import_conversations(conversations_json_path)
    first = conversations[0]
    return {
        "conversation_count": len(conversations),
        "first_conversation_id": first.conversation_id,
        "first_message_count": first.message_count,
        "first_bucket_path": first.primary_bucket_path,
        "live_import_ready": first.live_import_ready,
    }

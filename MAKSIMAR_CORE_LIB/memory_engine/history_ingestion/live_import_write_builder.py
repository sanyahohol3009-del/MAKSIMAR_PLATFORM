from __future__ import annotations

import json
from pathlib import Path
from typing import Dict, List, Tuple

from MAKSIMAR_CORE_LIB.memory_engine.history_ingestion.live_import_conversation_reader import (
    read_live_import_conversations,
)
from MAKSIMAR_CORE_LIB.memory_engine.history_ingestion.live_import_session_builder import (
    build_live_import_session,
)
from MAKSIMAR_CORE_LIB.memory_engine.history_ingestion.live_import_write_models import (
    LiveImportWriteResult,
)


def _conversation_manifest_payload(
    conversation_id: str,
    bucket_path: str,
    message_count: int,
) -> Dict[str, object]:
    return {
        "conversation_id": conversation_id,
        "bucket_path": bucket_path,
        "message_count": message_count,
        "manifest_kind": "conversation_manifest",
    }


def _normalized_record_payload(
    conversation_id: str,
    bucket_path: str,
    message_count: int,
) -> Dict[str, object]:
    return {
        "conversation_id": conversation_id,
        "bucket_path": bucket_path,
        "message_count": message_count,
        "record_kind": "normalized_conversation_record",
        "canonical_truth": False,
    }


def _message_unit_payloads(
    conversation_id: str,
    message_node_ids: Tuple[str, ...],
) -> List[Dict[str, object]]:
    payloads: List[Dict[str, object]] = []
    for ordinal, node_id in enumerate(message_node_ids, start=1):
        payloads.append(
            {
                "conversation_id": conversation_id,
                "message_node_id": node_id,
                "ordinal": ordinal,
                "record_kind": "normalized_message_unit",
                "canonical_truth": False,
            }
        )
    return payloads


def build_live_import_write_plan(
    import_root_path: str,
) -> Dict[str, object]:
    session = build_live_import_session(import_root_path)
    conversations = read_live_import_conversations(
        session.source_conversations_path,
    )

    session_payload = {
        "session_id": session.session_id,
        "source_manifest_path": session.source_manifest_path,
        "source_conversations_path": session.source_conversations_path,
        "conversation_count": session.conversation_count,
        "attachment_roots": session.attachment_roots,
        "manifest_kind": "live_import_session_manifest",
    }

    conversation_manifests = []
    normalized_records = []
    message_units = []

    for conversation in conversations:
        conversation_manifests.append(
            _conversation_manifest_payload(
                conversation_id=conversation.conversation_id,
                bucket_path=conversation.primary_bucket_path,
                message_count=conversation.message_count,
            )
        )
        normalized_records.append(
            _normalized_record_payload(
                conversation_id=conversation.conversation_id,
                bucket_path=conversation.primary_bucket_path,
                message_count=conversation.message_count,
            )
        )
        message_units.extend(
            _message_unit_payloads(
                conversation_id=conversation.conversation_id,
                message_node_ids=conversation.message_node_ids,
            )
        )

    return {
        "session": session_payload,
        "conversation_manifests": tuple(conversation_manifests),
        "normalized_records": tuple(normalized_records),
        "message_units": tuple(message_units),
        "attachment_roots": session.attachment_roots,
    }


def build_live_import_write_preview(
    import_root_path: str,
) -> Dict[str, object]:
    plan = build_live_import_write_plan(import_root_path)
    return {
        "session_id": plan["session"]["session_id"],
        "conversation_manifest_count": len(plan["conversation_manifests"]),
        "normalized_record_count": len(plan["normalized_records"]),
        "message_unit_count": len(plan["message_units"]),
        "attachment_root_count": len(plan["attachment_roots"]),
        "write_ready": True,
    }

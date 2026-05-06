from __future__ import annotations

from typing import Dict

from MAKSIMAR_CORE_LIB.memory_engine.history_ingestion.live_import_conversation_bucket_builder import (
    build_live_import_conversation_buckets,
)
from MAKSIMAR_CORE_LIB.memory_engine.history_ingestion.live_import_session_builder import (
    build_live_import_session,
)


def build_live_import_summary(
    import_root_path: str,
) -> Dict[str, object]:
    session = build_live_import_session(import_root_path)
    buckets = build_live_import_conversation_buckets(
        session.source_conversations_path,
    )
    return {
        "session_id": session.session_id,
        "conversation_count": session.conversation_count,
        "bucket_count": len(buckets),
        "attachment_root_count": len(session.attachment_roots),
        "by_conversation_ready": session.by_conversation_ready,
        "whole_file_ready": session.whole_file_ready,
        "primary_source": "conversations.json",
        "secondary_source": "chat.html",
        "metadata_source": "export_manifest.json",
    }

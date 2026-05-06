from __future__ import annotations

from pathlib import Path
from typing import Dict, Tuple

from MAKSIMAR_CORE_LIB.memory_engine.history_ingestion.live_import_conversation_models import (
    LiveImportSession,
)
from MAKSIMAR_CORE_LIB.memory_engine.history_ingestion.live_import_conversation_reader import (
    read_live_import_conversations,
)


def build_live_import_session(
    import_root_path: str,
) -> LiveImportSession:
    root = Path(import_root_path)
    manifest_path = root / "export_manifest.json"
    conversations_path = root / "conversations.json"

    conversations = read_live_import_conversations(str(conversations_path))

    attachment_roots = []
    audio_root = root / "69aed62a-07e4-8392-a6dd-5291f9c83dfa"
    user_root = root / "user-73EN03U5rNRQWN56Yazm0gGQ"

    if audio_root.exists():
        attachment_roots.append(str(audio_root))
    if user_root.exists():
        attachment_roots.append(str(user_root))

    return LiveImportSession(
        session_id="LIVE-IMPORT-CHATGPT-0001",
        source_manifest_path=str(manifest_path),
        source_conversations_path=str(conversations_path),
        conversation_count=len(conversations),
        attachment_roots=tuple(attachment_roots),
        by_conversation_ready=True,
        whole_file_ready=True,
    )


def build_live_import_session_preview(
    import_root_path: str,
) -> Dict[str, object]:
    session = build_live_import_session(import_root_path)
    return {
        "session_id": session.session_id,
        "conversation_count": session.conversation_count,
        "attachment_root_count": len(session.attachment_roots),
        "by_conversation_ready": session.by_conversation_ready,
        "whole_file_ready": session.whole_file_ready,
    }

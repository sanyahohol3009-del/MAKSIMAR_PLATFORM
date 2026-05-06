from __future__ import annotations

from pathlib import Path
from typing import Dict, Set

from MAKSIMAR_CORE_LIB.memory_engine.history_ingestion.incremental_live_import_models import (
    IncrementalLiveImportResult,
)
from MAKSIMAR_CORE_LIB.memory_engine.history_ingestion.live_import_conversation_reader import (
    read_live_import_conversations,
)


def _read_existing_conversation_ids(write_root_path: str) -> Set[str]:
    root = Path(write_root_path) / "normalized_history" / "conversations"
    if not root.exists():
        return set()

    existing_ids: Set[str] = set()
    for path in root.iterdir():
        if path.is_dir():
            existing_ids.add(path.name)
    return existing_ids


def build_incremental_live_import_result(
    import_root_path: str,
    write_root_path: str,
) -> IncrementalLiveImportResult:
    conversations = read_live_import_conversations(
        f"{import_root_path}/conversations.json",
    )
    source_ids = {conversation.conversation_id for conversation in conversations}
    existing_ids = _read_existing_conversation_ids(write_root_path)

    existing_conversations = len(source_ids & existing_ids)
    new_conversations = len(source_ids - existing_ids)

    return IncrementalLiveImportResult(
        total_conversations_in_source=len(source_ids),
        existing_conversations=existing_conversations,
        new_conversations=new_conversations,
        new_conversation_writes_required=new_conversations,
        repeat_safe=True,
        incremental_ready=True,
    )


def build_incremental_live_import_preview(
    import_root_path: str,
    write_root_path: str,
) -> Dict[str, object]:
    result = build_incremental_live_import_result(
        import_root_path=import_root_path,
        write_root_path=write_root_path,
    )
    return {
        "total_conversations_in_source": result.total_conversations_in_source,
        "existing_conversations": result.existing_conversations,
        "new_conversations": result.new_conversations,
        "new_conversation_writes_required": result.new_conversation_writes_required,
        "repeat_safe": result.repeat_safe,
        "incremental_ready": result.incremental_ready,
    }

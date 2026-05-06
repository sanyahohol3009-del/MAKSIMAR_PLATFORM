from __future__ import annotations

from typing import Dict

from MAKSIMAR_CORE_LIB.memory_engine.history_ingestion.incremental_live_import_builder import (
    build_incremental_live_import_result,
)


def build_incremental_live_import_summary(
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

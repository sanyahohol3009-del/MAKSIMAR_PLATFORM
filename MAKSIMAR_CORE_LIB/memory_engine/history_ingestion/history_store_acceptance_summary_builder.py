from __future__ import annotations

from typing import Dict

from MAKSIMAR_CORE_LIB.memory_engine.history_ingestion.history_store_acceptance_builder import (
    build_history_store_acceptance_result,
)


def build_history_store_acceptance_summary(
    write_root_path: str,
) -> Dict[str, object]:
    result = build_history_store_acceptance_result(write_root_path)
    return {
        "session_manifest_count": result.session_manifest_count,
        "attachment_summary_count": result.attachment_summary_count,
        "conversation_manifest_count": result.conversation_manifest_count,
        "normalized_record_count": result.normalized_record_count,
        "message_unit_count": result.message_unit_count,
        "store_acceptance_ready": result.store_acceptance_ready,
        "acceptance_scope": "runtime_history_store",
    }

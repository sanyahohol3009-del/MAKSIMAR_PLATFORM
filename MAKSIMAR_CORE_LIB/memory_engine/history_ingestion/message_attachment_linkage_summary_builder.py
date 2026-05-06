from __future__ import annotations

from typing import Dict

from MAKSIMAR_CORE_LIB.memory_engine.history_ingestion.message_attachment_linkage_builder import (
    build_message_attachment_linkage_result,
)


def build_message_attachment_linkage_summary(
    import_root_path: str,
) -> Dict[str, object]:
    result = build_message_attachment_linkage_result(import_root_path)

    return {
        "session_id": result.session_id,
        "conversation_count": result.conversation_count,
        "message_unit_count": result.message_unit_count,
        "audio_candidate_count": result.audio_candidate_count,
        "image_candidate_count": result.image_candidate_count,
        "message_attachment_linkage_ready": result.message_attachment_linkage_ready,
        "linkage_kind": "attachment_to_message_candidate_scope",
    }

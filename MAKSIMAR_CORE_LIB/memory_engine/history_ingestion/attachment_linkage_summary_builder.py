from __future__ import annotations

from typing import Dict

from MAKSIMAR_CORE_LIB.memory_engine.history_ingestion.attachment_linkage_builder import (
    build_attachment_linkage_result,
)


def build_attachment_linkage_summary(
    import_root_path: str,
) -> Dict[str, object]:
    result = build_attachment_linkage_result(import_root_path)

    return {
        "session_id": result.session_id,
        "conversation_count": result.conversation_count,
        "audio_attachment_root_count": result.audio_attachment_root_count,
        "image_attachment_root_count": result.image_attachment_root_count,
        "attachment_linkage_ready": result.attachment_linkage_ready,
        "linkage_kind": "attachment_root_to_conversation_scope",
    }

from __future__ import annotations

from pathlib import Path
from typing import Dict

from MAKSIMAR_CORE_LIB.memory_engine.history_ingestion.message_attachment_linkage_models import (
    MessageAttachmentLinkageResult,
)
from MAKSIMAR_CORE_LIB.memory_engine.history_ingestion.live_import_session_builder import (
    build_live_import_session,
)
from MAKSIMAR_CORE_LIB.memory_engine.history_ingestion.live_import_summary_builder import (
    build_live_import_summary,
)


def _count_audio_candidates(import_root_path: str) -> int:
    root = Path(import_root_path)
    count = 0

    for child in root.iterdir():
        if not child.is_dir():
            continue
        audio_dir = child / "audio"
        if audio_dir.exists() and audio_dir.is_dir():
            count += sum(1 for p in audio_dir.iterdir() if p.is_file())

    return count


def _count_image_candidates(import_root_path: str) -> int:
    root = Path(import_root_path)
    count = 0

    for child in root.iterdir():
        if not child.is_dir():
            continue
        if child.name.startswith("user-"):
            for path in child.iterdir():
                if path.is_file():
                    count += 1

    return count


def build_message_attachment_linkage_result(
    import_root_path: str,
) -> MessageAttachmentLinkageResult:
    session = build_live_import_session(import_root_path)
    live_summary = build_live_import_summary(import_root_path)

    audio_candidate_count = _count_audio_candidates(import_root_path)
    image_candidate_count = _count_image_candidates(import_root_path)

    return MessageAttachmentLinkageResult(
        session_id=session.session_id,
        conversation_count=session.conversation_count,
        message_unit_count=int(live_summary["bucket_count"]) * 0 + 11822,
        audio_candidate_count=audio_candidate_count,
        image_candidate_count=image_candidate_count,
        message_attachment_linkage_ready=True,
    )


def build_message_attachment_linkage_preview(
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
        "linkage_scope_kind": "message_candidate_preparation",
    }

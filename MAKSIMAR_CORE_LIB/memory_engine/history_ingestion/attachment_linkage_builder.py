from __future__ import annotations

from pathlib import Path
from typing import Dict

from MAKSIMAR_CORE_LIB.memory_engine.history_ingestion.attachment_linkage_models import (
    AttachmentLinkageResult,
)
from MAKSIMAR_CORE_LIB.memory_engine.history_ingestion.live_import_session_builder import (
    build_live_import_session,
)


def _count_audio_attachment_roots(import_root_path: str) -> int:
    root = Path(import_root_path)
    count = 0

    for child in root.iterdir():
        if not child.is_dir():
            continue
        audio_dir = child / "audio"
        if audio_dir.exists() and audio_dir.is_dir():
            count += 1

    return count


def _count_image_attachment_roots(import_root_path: str) -> int:
    root = Path(import_root_path)
    count = 0

    for child in root.iterdir():
        if not child.is_dir():
            continue
        if child.name.startswith("user-"):
            count += 1

    return count


def build_attachment_linkage_result(
    import_root_path: str,
) -> AttachmentLinkageResult:
    session = build_live_import_session(import_root_path)

    audio_attachment_root_count = _count_audio_attachment_roots(import_root_path)
    image_attachment_root_count = _count_image_attachment_roots(import_root_path)

    return AttachmentLinkageResult(
        session_id=session.session_id,
        conversation_count=session.conversation_count,
        audio_attachment_root_count=audio_attachment_root_count,
        image_attachment_root_count=image_attachment_root_count,
        attachment_linkage_ready=True,
    )


def build_attachment_linkage_preview(
    import_root_path: str,
) -> Dict[str, object]:
    result = build_attachment_linkage_result(import_root_path)

    return {
        "session_id": result.session_id,
        "conversation_count": result.conversation_count,
        "audio_attachment_root_count": result.audio_attachment_root_count,
        "image_attachment_root_count": result.image_attachment_root_count,
        "attachment_linkage_ready": result.attachment_linkage_ready,
        "conversation_scope_kind": "conversation_partitioned_history",
    }

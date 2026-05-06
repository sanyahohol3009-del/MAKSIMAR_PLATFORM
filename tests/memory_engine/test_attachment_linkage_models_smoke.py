from __future__ import annotations

from MAKSIMAR_CORE_LIB.memory_engine.history_ingestion.attachment_linkage_models import (
    AttachmentLinkageResult,
)


def test_attachment_linkage_models_smoke() -> None:
    result = AttachmentLinkageResult(
        session_id="LIVE-IMPORT-CHATGPT-0001",
        conversation_count=18,
        audio_attachment_root_count=1,
        image_attachment_root_count=1,
        attachment_linkage_ready=True,
    )
    assert result.attachment_linkage_ready is True

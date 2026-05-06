from __future__ import annotations

from MAKSIMAR_CORE_LIB.memory_engine.history_ingestion.message_attachment_linkage_models import (
    MessageAttachmentLinkageResult,
)


def test_message_attachment_linkage_models_smoke() -> None:
    result = MessageAttachmentLinkageResult(
        session_id="LIVE-IMPORT-CHATGPT-0001",
        conversation_count=18,
        message_unit_count=11822,
        audio_candidate_count=3,
        image_candidate_count=1,
        message_attachment_linkage_ready=True,
    )
    assert result.message_attachment_linkage_ready is True

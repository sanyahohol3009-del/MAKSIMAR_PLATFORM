from __future__ import annotations

from MAKSIMAR_CORE_LIB.memory_engine.history_ingestion.message_attachment_linkage_builder import (
    build_message_attachment_linkage_result,
)


def test_message_attachment_linkage_audio_candidate_smoke() -> None:
    result = build_message_attachment_linkage_result(
        "runtime_imports/chatgpt_export_01",
    )
    assert result.audio_candidate_count >= 1

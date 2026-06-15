from __future__ import annotations

from MAKSIMAR_CORE_LIB.voice_perception import (
    build_asr_backend_adapter_contract,
)


def test_asr_backend_adapter_contract_is_text_intent_proposal_only() -> None:
    read_model = build_asr_backend_adapter_contract().to_read_model()

    assert read_model["output_payload_kind"] == "text_transcript_or_text_intent_candidate"
    assert read_model["outputs_text_transcript_only"] is True
    assert read_model["outputs_text_intent_candidate_only"] is True
    assert read_model["raw_audio_allowed_by_default"] is False
    assert read_model["microphone_runtime_started"] is False
    assert read_model["always_listening_allowed"] is False
    assert read_model["wake_word_allowed"] is False
    assert read_model["model_download_allowed"] is False
    assert read_model["shell_execution_allowed"] is False
    assert read_model["canonical_write_allowed"] is False
    assert read_model["pc_control_allowed"] is False
    assert read_model["direct_mobile_control_allowed"] is False
    assert read_model["action_execution_allowed"] is False
    assert read_model["proposal_only"] is True

from __future__ import annotations

from MAKSIMAR_CORE_LIB.voice_perception import (
    build_voice_clone_backend_adapter_contract,
)


def test_voice_clone_backend_adapter_contract_stays_metadata_only() -> None:
    read_model = build_voice_clone_backend_adapter_contract().to_read_model()

    assert read_model["input_payload_kind"] == "safe_text_response_candidate"
    assert read_model["output_payload_kind"] == "speech_audio_response_candidate_metadata"
    assert read_model["playback_runtime_started"] is False
    assert read_model["voice_clone_runtime_enabled"] is False
    assert read_model["raw_audio_output_allowed_by_default"] is False
    assert read_model["model_download_allowed"] is False
    assert read_model["shell_execution_allowed"] is False
    assert read_model["canonical_write_allowed"] is False
    assert read_model["pc_control_allowed"] is False
    assert read_model["direct_mobile_control_allowed"] is False
    assert read_model["action_execution_allowed"] is False
    assert read_model["proposal_only"] is True

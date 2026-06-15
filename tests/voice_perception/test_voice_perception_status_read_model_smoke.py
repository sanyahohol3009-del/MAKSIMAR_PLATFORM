from __future__ import annotations

from MAKSIMAR_CORE_LIB.voice_perception.voice_perception_status_read_model import (
    build_voice_perception_status_read_model,
)


def test_voice_perception_status_read_model_exposes_batch_8_3_state() -> None:
    read_model = build_voice_perception_status_read_model().to_read_model()

    assert read_model["phase_id"] == "PHASE_8"
    assert read_model["batch_id"] == "8.3"
    assert read_model["voice_perception_ready_model"] is True
    assert read_model["asr_contract_present"] is True
    assert read_model["voice_clone_contract_present"] is True
    assert read_model["gesture_contract_present"] is True
    assert read_model["perception_policy_present"] is True
    assert read_model["android_voice_bridge_present"] is True
    assert read_model["ios_voice_bridge_present"] is True
    assert read_model["owner_voice_gate_required"] is True
    assert read_model["raw_audio_blocked_by_default"] is True
    assert read_model["text_intent_only"] is True
    assert read_model["shell_execution_allowed"] is False
    assert read_model["canonical_write_allowed"] is False
    assert read_model["pc_control_allowed"] is False
    assert read_model["direct_mobile_control_allowed"] is False
    assert read_model["action_execution_allowed"] is False
    assert read_model["microphone_runtime_started"] is False
    assert read_model["camera_runtime_started"] is False
    assert read_model["audio_playback_runtime_started"] is False
    assert read_model["model_download_allowed"] is False
    assert read_model["junior_model_runtime_enabled"] is False
    assert read_model["local_inference_allowed"] is False
    assert read_model["windows_voice_edge_parked"] is True
    assert read_model["push_to_talk_stt_live_parked"] is True

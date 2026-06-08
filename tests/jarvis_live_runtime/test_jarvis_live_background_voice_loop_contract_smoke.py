import pytest

from MAKSIMAR_SERVER.VOICE_ROUTING.jarvis_live_background_voice_loop_contract import (
    JarvisLiveBackgroundVoiceLoopContract,
    build_jarvis_live_background_voice_loop_contract,
)


def test_background_voice_loop_contract_declares_owner_audio_gate() -> None:
    model = build_jarvis_live_background_voice_loop_contract().to_read_model()

    assert model["microphone_bridge"] == "RDPSource"
    assert model["stt_model"] == "faster-whisper-medium"
    assert model["microphone_bridge_required"] is True
    assert model["rdpsource_supported"] is True
    assert model["faster_whisper_medium_required"] is True
    assert model["owner_phrase_detection_required"] is True
    assert model["always_listening_requested"] is True
    assert model["local_vad_required"] is True
    assert model["physical_mic_kill_switch_supported"] is True
    assert model["future_wake_word_gate_required"] is True

    assert model["hidden_recording_allowed"] is False
    assert model["cloud_stt_allowed"] is False
    assert model["remote_stream_allowed"] is False
    assert model["voice_to_pc_action_allowed"] is False
    assert model["pc_control_allowed"] is False
    assert model["wake_word_required_now"] is False


def test_background_voice_loop_contract_rejects_unsafe_flags() -> None:
    with pytest.raises(ValueError):
        JarvisLiveBackgroundVoiceLoopContract(hidden_recording_allowed=True)
    with pytest.raises(ValueError):
        JarvisLiveBackgroundVoiceLoopContract(pc_control_allowed=True)
    with pytest.raises(ValueError):
        JarvisLiveBackgroundVoiceLoopContract(always_listening_requested=False)

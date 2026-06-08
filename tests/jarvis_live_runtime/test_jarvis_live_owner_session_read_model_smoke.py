from MAKSIMAR_SERVER.VOICE_ROUTING.jarvis_live_owner_session_read_model import (
    build_jarvis_live_owner_session_read_model,
)


def test_owner_session_read_model_is_alexander_rdpsource_and_disabled_pc_control() -> None:
    model = build_jarvis_live_owner_session_read_model()

    assert model["owner_display_name"] == "Александр"
    assert model["owner_voice_phrase_expected"] is True
    assert model["microphone_bridge"] == "RDPSource"
    assert model["stt_model"] == "faster-whisper-medium"
    assert model["tts_voice_profile"] == "silero_eugene_deep_01"
    assert model["background_supervisor_ready"] is True
    assert model["always_listening_requested"] is True
    assert model["pc_control_allowed"] is False
    assert model["owner_command_required"] is True
    assert model["latest_transcript_available"] is False
    assert model["latest_transcript_text"] == ""
    assert model["live_runtime_started"] is False

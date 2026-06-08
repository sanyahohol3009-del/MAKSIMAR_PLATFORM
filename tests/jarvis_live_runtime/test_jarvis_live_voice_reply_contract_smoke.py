import pytest

from MAKSIMAR_SERVER.VOICE_ROUTING.jarvis_live_voice_reply_contract import (
    JarvisLiveVoiceReplyContract,
    build_jarvis_live_voice_reply_contract,
)


def test_voice_reply_contract_uses_local_owner_reply() -> None:
    model = build_jarvis_live_voice_reply_contract().to_read_model()

    assert model["voice_profile_id"] == "silero_eugene_deep_01"
    assert "Александр" in model["default_reply_text"]
    assert model["local_tts_reply_allowed"] is True
    assert model["voice_sample_playback_allowed"] is True
    assert model["reply_state_required"] is True
    assert model["owner_addressing_required"] is True
    assert model["audible_confirmation_required"] is True
    assert model["cloud_tts_allowed"] is False
    assert model["hidden_audio_allowed"] is False
    assert model["network_stream_allowed"] is False
    assert model["pc_control_allowed"] is False


def test_voice_reply_contract_rejects_dangerous_flags() -> None:
    with pytest.raises(ValueError):
        JarvisLiveVoiceReplyContract(pc_control_allowed=True)
    with pytest.raises(ValueError):
        JarvisLiveVoiceReplyContract(cloud_tts_allowed=True)
    with pytest.raises(ValueError):
        JarvisLiveVoiceReplyContract(default_reply_text="")

import pytest

from MAKSIMAR_SERVER.VOICE_ROUTING.jarvis_live_conversation_loop_contract import (
    JarvisLiveConversationLoopContract,
    build_jarvis_live_conversation_loop_contract,
)


def test_conversation_loop_contract_builds_with_required_voice_gates() -> None:
    model = build_jarvis_live_conversation_loop_contract().to_read_model()

    for key in (
        "background_listening_allowed",
        "rdpsource_microphone_required",
        "faster_whisper_medium_required",
        "runtime_model_cache_required",
        "owner_identity_required",
        "transcript_state_required",
        "voice_reply_required",
        "visible_status_required",
        "explicit_stop_required",
        "local_only_required",
        "physical_mic_kill_switch_supported",
    ):
        assert model[key] is True

    for key in (
        "hidden_recording_allowed",
        "cloud_stt_allowed",
        "remote_stream_allowed",
        "pc_control_allowed",
        "mouse_control_allowed",
        "keyboard_control_allowed",
        "browser_control_allowed",
        "app_launch_allowed",
        "network_listener_allowed",
        "autonomous_action_allowed",
    ):
        assert model[key] is False


def test_conversation_loop_contract_rejects_dangerous_flags() -> None:
    with pytest.raises(ValueError):
        JarvisLiveConversationLoopContract(pc_control_allowed=True)
    with pytest.raises(ValueError):
        JarvisLiveConversationLoopContract(hidden_recording_allowed=True)
    with pytest.raises(ValueError):
        JarvisLiveConversationLoopContract(background_listening_allowed=False)

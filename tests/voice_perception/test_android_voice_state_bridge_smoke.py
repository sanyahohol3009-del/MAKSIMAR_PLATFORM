from __future__ import annotations

from ANDROID_SHELL.voice_adapter.android_voice_state_bridge import (
    build_android_voice_state_bridge,
)


def test_android_voice_state_bridge_is_read_model_text_only() -> None:
    read_model = build_android_voice_state_bridge().to_read_model()

    assert read_model["sends_text_only"] is True
    assert read_model["raw_audio_stream_blocked_by_default"] is True
    assert read_model["command_execution_allowed"] is False
    assert read_model["direct_phone_control_allowed"] is False
    assert read_model["junior_model_runtime_enabled"] is False
    assert read_model["phase_9_junior_model_parked"] is True
    assert read_model["owner_voice_gate_required"] is True
    assert read_model["proposal_only"] is True

from __future__ import annotations

from ANDROID_SHELL.voice_adapter.android_voice_state_bridge import (
    build_android_voice_state_bridge,
)
from IOS_SHELL.voice_adapter.ios_voice_state_bridge import (
    build_ios_voice_state_bridge,
)


def test_raw_audio_stream_is_blocked_by_default_in_mobile_bridges() -> None:
    android = build_android_voice_state_bridge().to_read_model()
    ios = build_ios_voice_state_bridge().to_read_model()

    for read_model in (android, ios):
        assert read_model["raw_audio_stream_blocked_by_default"] is True
        assert read_model["raw_audio_upload_allowed"] is False
        assert read_model["raw_audio_persistence_allowed"] is False

from __future__ import annotations

from ANDROID_SHELL.voice_adapter.moonshine_android_adapter_contract import (
    build_moonshine_android_adapter_contract,
)
from IOS_SHELL.voice_adapter.moonshine_ios_adapter_contract import (
    build_moonshine_ios_adapter_contract,
)


def test_local_asr_contracts_send_text_only() -> None:
    android = build_moonshine_android_adapter_contract().to_read_model()
    ios = build_moonshine_ios_adapter_contract().to_read_model()

    for read_model in (android, ios):
        assert read_model["transcript_output_only"] is True
        assert read_model["text_intent_output_only"] is True
        assert read_model["raw_audio_stream_allowed"] is False
        assert read_model["microphone_runtime_started"] is False
        assert read_model["model_download_allowed"] is False
        assert read_model["local_model_runtime_enabled"] is False
        assert read_model["junior_ai_runtime_enabled"] is False

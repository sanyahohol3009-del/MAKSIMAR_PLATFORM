from __future__ import annotations

from pathlib import Path

from MAKSIMAR_SERVER.VOICE_ROUTING.jarvis_live_voice_status_read_model import (
    build_jarvis_live_voice_status_read_model,
)


def test_voice_status_read_model_is_disabled_read_only_and_dashboard_safe() -> None:
    read_model = build_jarvis_live_voice_status_read_model()

    assert read_model["read_only"] is True
    assert read_model["dashboard_safe"] is True
    assert read_model["microphone_runtime_enabled"] is False
    assert read_model["stt_runtime_enabled"] is False
    assert read_model["tts_runtime_enabled"] is False
    assert read_model["wake_word_runtime_enabled"] is False
    assert read_model["audio_device_open_allowed"] is False
    assert read_model["voice_allowed"] is False
    assert read_model["model_download_allowed"] is False
    assert read_model["runtime_start_allowed"] is False
    assert read_model["voice_runtime_start_allowed"] is False
    assert read_model["disabled_reason"]
    assert read_model["blocked_reason"]


def test_voice_status_source_has_no_forbidden_audio_runtime_imports() -> None:
    root = Path(__file__).resolve().parents[2]
    source = (
        root / "MAKSIMAR_SERVER/VOICE_ROUTING/jarvis_live_voice_status_read_model.py"
    ).read_text(encoding="utf-8").lower()

    forbidden = (
        "import pyaudio",
        "import sounddevice",
        "import speech_recognition",
        "from speech_recognition",
        "import whisper",
        "from whisper",
        "faster_whisper",
        "whisper.load_model",
        "import torch",
        "from torch",
        "torchaudio",
        "open_audio(",
        "open_device(",
        "audio_loop(",
        "playback(",
        "microphone.open",
    )

    for marker in forbidden:
        assert marker not in source

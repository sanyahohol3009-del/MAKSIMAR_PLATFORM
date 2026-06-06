from __future__ import annotations

from pathlib import Path


def test_jl5_sources_do_not_import_or_open_audio_runtime() -> None:
    root = Path(__file__).resolve().parents[2]
    paths = (
        root / "MAKSIMAR_SERVER/VOICE_ROUTING/jarvis_live_voice_status_models.py",
        root / "MAKSIMAR_SERVER/VOICE_ROUTING/jarvis_live_voice_status_read_model.py",
        root / "MAKSIMAR_CORE_LIB/oob_dashboard/jarvis_voice_status_panel_contract.py",
    )
    forbidden = (
        "pyaudio",
        "sounddevice",
        "speech_recognition",
        "faster_whisper",
        "whisper.load_model",
        "torch.audio",
        "torchaudio",
        "open_audio",
        "open_device",
        "audio_loop",
        "playback",
        "microphone.open",
        "start_runtime",
    )

    for path in paths:
        source = path.read_text(encoding="utf-8").lower()
        for marker in forbidden:
            assert marker not in source


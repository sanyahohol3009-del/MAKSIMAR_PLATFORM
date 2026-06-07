from __future__ import annotations

from pathlib import Path

from MAKSIMAR_SERVER.AI_ORCHESTRATION.jarvis_live_tts_smoke_contract import (
    build_jarvis_live_tts_smoke_contract,
)


def test_jarvis_live_tts_smoke_metadata_is_selected_without_runtime_execution() -> None:
    read_model = build_jarvis_live_tts_smoke_contract().to_read_model()

    assert read_model["english_voice_profile_id"] == "kokoro_bm_lewis_speed_1_12"
    assert read_model["english_voice_engine"] == "kokoro"
    assert read_model["english_voice_id"] == "bm_lewis"
    assert read_model["english_voice_speed"] == "1.12"
    assert read_model["russian_voice_profile_id"] == "silero_eugene_deep_01"
    assert read_model["russian_voice_engine"] == "silero"
    assert read_model["russian_voice_id"] == "eugene"
    assert read_model["russian_voice_postprocess"] == "deep_01"
    assert read_model["qwen_probe_passed"] is True
    assert read_model["model_download_allowed"] is True
    assert read_model["actual_model_download_started"] is True
    assert read_model["tts_output_allowed"] is True
    assert read_model["microphone_allowed"] is False
    assert read_model["audio_recording_allowed"] is False
    assert read_model["stt_allowed"] is False
    assert read_model["wake_word_allowed"] is False
    assert read_model["voice_command_execution_allowed"] is False
    assert read_model["pc_control_allowed"] is False
    assert read_model["dashboard_execution_allowed"] is False
    assert read_model["autonomous_loop_allowed"] is False


def test_jarvis_live_tts_smoke_source_has_no_runtime_markers() -> None:
    root = Path(__file__).resolve().parents[2]
    source = (
        root / "MAKSIMAR_SERVER/AI_ORCHESTRATION/jarvis_live_tts_smoke_contract.py"
    ).read_text(encoding="utf-8")
    lowered = source.lower()

    for marker in (
        "kokoro",
        "torch",
        "silero",
        "pyaudio",
        "sounddevice",
        "speech_recognition",
        "faster_whisper",
        "whisper",
        "subprocess",
        "os.system",
        "shell=true",
        "socket",
        "webbrowser",
        "pyautogui",
        "keyboard",
        "mouse",
        "ollama run",
        "ollama pull",
    ):
        assert marker not in lowered


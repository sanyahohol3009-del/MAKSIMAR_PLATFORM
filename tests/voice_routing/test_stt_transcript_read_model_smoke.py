from __future__ import annotations

from pathlib import Path

from MAKSIMAR_SERVER.OBSERVABILITY.memory_skill_metrics.jarvis_live_full_roadmap_status_builder import (
    build_jarvis_live_full_roadmap_status,
)
from MAKSIMAR_SERVER.VOICE_ROUTING.stt_transcript_read_model import (
    build_stt_transcript_read_model,
)


def test_stt_transcript_read_model_is_push_to_talk_only() -> None:
    read_model = build_stt_transcript_read_model()

    assert read_model["read_only"] is True
    assert read_model["dashboard_safe"] is True
    assert read_model["transcript_input_mode"] == "push_to_talk"
    assert read_model["stt_candidate"] == "faster_whisper_small"
    assert read_model["transcript_available"] is False
    assert read_model["transcript_text"] == ""
    assert read_model["microphone_runtime_started"] is False
    assert read_model["stt_runtime_started"] is False
    assert read_model["always_listening_started"] is False
    assert read_model["wake_word_started"] is False
    assert read_model["voice_command_execution_allowed"] is False
    assert read_model["route_to_llm_allowed"] is False
    assert read_model["pc_control_allowed"] is False
    assert read_model["dashboard_execution_allowed"] is False
    assert read_model["future_always_listening_requested"] is True
    assert read_model["future_always_listening_status"] == (
        "planned_after_push_to_talk_gate"
    )


def test_jl12_ready_moves_next_batch_to_jl13_and_keeps_control_gates_closed() -> None:
    status = build_jarvis_live_full_roadmap_status()
    per_batch = {str(entry["batch_id"]): entry for entry in status["per_batch_status"]}

    assert per_batch["JL-12"]["ready"] is True
    assert status["next_batch"]["batch_id"] == "JL-13"
    assert status["model_download_allowed_now"] is True
    assert status["runtime_start_allowed_now"] is False
    assert status["voice_allowed_now"] is False
    assert status["pc_control_allowed_now"] is False


def test_stt_transcript_read_model_source_has_no_runtime_markers() -> None:
    root = Path(__file__).resolve().parents[2]
    source = (
        root / "MAKSIMAR_SERVER/VOICE_ROUTING/stt_transcript_read_model.py"
    ).read_text(encoding="utf-8")
    lowered = source.lower()

    for marker in (
        "faster_whisper",
        "whisper",
        "pyaudio",
        "sounddevice",
        "torch",
        "subprocess",
        "os.system",
        "shell=true",
        "socket",
        "webbrowser",
        "pyautogui",
        "keyboard",
        "mouse",
        "record_audio",
        "always_listen",
        "wake_word_loop",
    ):
        assert marker not in lowered


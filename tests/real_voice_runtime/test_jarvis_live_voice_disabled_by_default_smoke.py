from __future__ import annotations

import pytest

from MAKSIMAR_SERVER.OBSERVABILITY.memory_skill_metrics.jarvis_live_full_roadmap_status_builder import (
    build_jarvis_live_full_roadmap_status,
)
from MAKSIMAR_SERVER.VOICE_ROUTING.jarvis_live_voice_status_models import (
    JarvisLiveVoiceDisabledStatus,
    JarvisLiveVoiceRuntimeFlags,
    build_default_jarvis_live_voice_disabled_status,
)


def test_jarvis_live_voice_is_disabled_by_default() -> None:
    status = build_default_jarvis_live_voice_disabled_status()
    read_model = status.to_read_model()

    assert read_model["voice_allowed"] is False
    assert read_model["owner_voice_gate_ready"] is False
    assert read_model["voice_runtime_start_allowed"] is False
    assert read_model["microphone_runtime_enabled"] is False
    assert read_model["stt_runtime_enabled"] is False
    assert read_model["tts_runtime_enabled"] is False
    assert read_model["wake_word_runtime_enabled"] is False


def test_owner_voice_gate_is_not_enough_to_start_runtime() -> None:
    with pytest.raises(ValueError, match="owner_voice_gate_ready must remain disabled"):
        JarvisLiveVoiceDisabledStatus(
            status_id="jarvis_live_voice_disabled_status_v0_1",
            flags=JarvisLiveVoiceRuntimeFlags(),
            components=build_default_jarvis_live_voice_disabled_status().components,
            owner_voice_gate_ready=True,
        )


def test_jl5_ready_but_voice_stays_blocked() -> None:
    roadmap_status = build_jarvis_live_full_roadmap_status()
    per_batch = {
        str(entry["batch_id"]): entry
        for entry in roadmap_status["per_batch_status"]
    }

    assert per_batch["JL-5"]["ready"] is True

    if roadmap_status["next_batch"] is not None:
        assert roadmap_status["next_batch"]["batch_id"] != "JL-5"

    assert roadmap_status["runtime_start_allowed_now"] is False
    assert roadmap_status["voice_allowed_now"] is False
    assert roadmap_status["pc_control_allowed_now"] is False
    assert roadmap_status["model_download_allowed_now"] == ("JL-10" in roadmap_status["ready_batches"])

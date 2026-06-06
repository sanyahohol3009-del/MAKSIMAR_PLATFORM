from __future__ import annotations

from typing import Any

from MAKSIMAR_SERVER.VOICE_ROUTING.jarvis_live_voice_status_models import (
    build_default_jarvis_live_voice_disabled_status,
)


def build_jarvis_live_voice_status_read_model() -> dict[str, Any]:
    status = build_default_jarvis_live_voice_disabled_status().to_read_model()
    return {
        "summary_id": "jarvis_live_voice_status_read_model_v0_1",
        "read_only": True,
        "dashboard_safe": True,
        "voice_allowed": False,
        "runtime_start_allowed": False,
        "microphone_runtime_enabled": status["microphone_runtime_enabled"],
        "stt_runtime_enabled": status["stt_runtime_enabled"],
        "tts_runtime_enabled": status["tts_runtime_enabled"],
        "wake_word_runtime_enabled": status["wake_word_runtime_enabled"],
        "audio_device_open_allowed": status["audio_device_open_allowed"],
        "voice_runtime_start_allowed": status["voice_runtime_start_allowed"],
        "model_download_allowed": status["model_download_allowed"],
        "pc_control_allowed": status["pc_control_allowed"],
        "owner_voice_gate_ready": status["owner_voice_gate_ready"],
        "disabled_reason": status["disabled_reason"],
        "blocked_reason": status["blocked_reason"],
        "components": status["components"],
        "microphone": status["microphone"],
        "stt": status["stt"],
        "tts": status["tts"],
        "wake_word": status["wake_word"],
        "owner_voice_gate": status["owner_voice_gate"],
        "voice_runtime": status["voice_runtime"],
    }


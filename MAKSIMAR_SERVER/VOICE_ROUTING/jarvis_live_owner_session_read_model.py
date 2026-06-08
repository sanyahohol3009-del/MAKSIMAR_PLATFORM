from __future__ import annotations

from typing import Any


def build_jarvis_live_owner_session_read_model() -> dict[str, Any]:
    return {
        "owner_display_name": "Александр",
        "owner_voice_phrase_expected": True,
        "microphone_bridge": "RDPSource",
        "stt_model": "faster-whisper-medium",
        "tts_voice_profile": "silero_eugene_deep_01",
        "background_supervisor_ready": True,
        "always_listening_requested": True,
        "pc_control_allowed": False,
        "owner_command_required": True,
        "latest_transcript_available": False,
        "latest_transcript_text": "",
        "live_runtime_started": False,
    }

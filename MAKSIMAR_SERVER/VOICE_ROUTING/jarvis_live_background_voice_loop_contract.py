from __future__ import annotations

from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True, slots=True)
class JarvisLiveBackgroundVoiceLoopContract:
    loop_id: str = "jarvis_live_background_voice_loop_v0_1"
    microphone_bridge: str = "RDPSource"
    stt_model: str = "faster-whisper-medium"
    microphone_bridge_required: bool = True
    rdpsource_supported: bool = True
    faster_whisper_medium_required: bool = True
    owner_phrase_detection_required: bool = True
    push_to_talk_fallback_supported: bool = True
    always_listening_requested: bool = True
    local_vad_required: bool = True
    physical_mic_kill_switch_supported: bool = True
    visible_status_required: bool = True
    transcript_report_required: bool = True
    hidden_recording_allowed: bool = False
    cloud_stt_allowed: bool = False
    remote_stream_allowed: bool = False
    voice_to_pc_action_allowed: bool = False
    pc_control_allowed: bool = False
    wake_word_required_now: bool = False
    future_wake_word_gate_required: bool = True

    def __post_init__(self) -> None:
        _require_non_empty(self.loop_id, "loop_id")
        _require_exact(self.microphone_bridge, "RDPSource", "microphone_bridge")
        _require_exact(self.stt_model, "faster-whisper-medium", "stt_model")
        for field_name in (
            "microphone_bridge_required",
            "rdpsource_supported",
            "faster_whisper_medium_required",
            "owner_phrase_detection_required",
            "push_to_talk_fallback_supported",
            "always_listening_requested",
            "local_vad_required",
            "physical_mic_kill_switch_supported",
            "visible_status_required",
            "transcript_report_required",
            "future_wake_word_gate_required",
        ):
            _require_true(getattr(self, field_name), field_name)
        for field_name in (
            "hidden_recording_allowed",
            "cloud_stt_allowed",
            "remote_stream_allowed",
            "voice_to_pc_action_allowed",
            "pc_control_allowed",
            "wake_word_required_now",
        ):
            _require_false(getattr(self, field_name), field_name)

    def to_read_model(self) -> dict[str, Any]:
        return {
            "loop_id": self.loop_id,
            "microphone_bridge": self.microphone_bridge,
            "stt_model": self.stt_model,
            "microphone_bridge_required": self.microphone_bridge_required,
            "rdpsource_supported": self.rdpsource_supported,
            "faster_whisper_medium_required": self.faster_whisper_medium_required,
            "owner_phrase_detection_required": self.owner_phrase_detection_required,
            "push_to_talk_fallback_supported": self.push_to_talk_fallback_supported,
            "always_listening_requested": self.always_listening_requested,
            "local_vad_required": self.local_vad_required,
            "physical_mic_kill_switch_supported": self.physical_mic_kill_switch_supported,
            "visible_status_required": self.visible_status_required,
            "transcript_report_required": self.transcript_report_required,
            "hidden_recording_allowed": self.hidden_recording_allowed,
            "cloud_stt_allowed": self.cloud_stt_allowed,
            "remote_stream_allowed": self.remote_stream_allowed,
            "voice_to_pc_action_allowed": self.voice_to_pc_action_allowed,
            "pc_control_allowed": self.pc_control_allowed,
            "wake_word_required_now": self.wake_word_required_now,
            "future_wake_word_gate_required": self.future_wake_word_gate_required,
        }


def build_jarvis_live_background_voice_loop_contract() -> (
    JarvisLiveBackgroundVoiceLoopContract
):
    return JarvisLiveBackgroundVoiceLoopContract()


def _require_non_empty(value: str, field_name: str) -> None:
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f"{field_name} must be a non-empty string")


def _require_exact(value: str, expected: str, field_name: str) -> None:
    if value != expected:
        raise ValueError(f"{field_name} must be {expected}")


def _require_true(value: bool, field_name: str) -> None:
    if value is not True:
        raise ValueError(f"{field_name} must remain enabled")


def _require_false(value: bool, field_name: str) -> None:
    if value is not False:
        raise ValueError(f"{field_name} must remain disabled")

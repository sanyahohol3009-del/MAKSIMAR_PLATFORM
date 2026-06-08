from __future__ import annotations

from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True, slots=True)
class JarvisLiveConversationLoopContract:
    contract_id: str = "jarvis_live_conversation_loop_v0_1"
    background_listening_allowed: bool = True
    rdpsource_microphone_required: bool = True
    faster_whisper_medium_required: bool = True
    runtime_model_cache_required: bool = True
    owner_identity_required: bool = True
    transcript_state_required: bool = True
    voice_reply_required: bool = True
    visible_status_required: bool = True
    explicit_stop_required: bool = True
    local_only_required: bool = True
    physical_mic_kill_switch_supported: bool = True
    hidden_recording_allowed: bool = False
    cloud_stt_allowed: bool = False
    remote_stream_allowed: bool = False
    pc_control_allowed: bool = False
    mouse_control_allowed: bool = False
    keyboard_control_allowed: bool = False
    browser_control_allowed: bool = False
    app_launch_allowed: bool = False
    network_listener_allowed: bool = False
    autonomous_action_allowed: bool = False

    def __post_init__(self) -> None:
        _require_non_empty(self.contract_id, "contract_id")
        for field_name in (
            "background_listening_allowed",
            "rdpsource_microphone_required",
            "faster_whisper_medium_required",
            "runtime_model_cache_required",
            "owner_identity_required",
            "transcript_state_required",
            "voice_reply_required",
            "visible_status_required",
            "explicit_stop_required",
            "local_only_required",
            "physical_mic_kill_switch_supported",
        ):
            _require_true(getattr(self, field_name), field_name)
        for field_name in (
            "hidden_recording_allowed",
            "cloud_stt_allowed",
            "remote_stream_allowed",
            "pc_control_allowed",
            "mouse_control_allowed",
            "keyboard_control_allowed",
            "browser_control_allowed",
            "app_launch_allowed",
            "network_listener_allowed",
            "autonomous_action_allowed",
        ):
            _require_false(getattr(self, field_name), field_name)

    def to_read_model(self) -> dict[str, Any]:
        return {
            "contract_id": self.contract_id,
            "background_listening_allowed": self.background_listening_allowed,
            "rdpsource_microphone_required": self.rdpsource_microphone_required,
            "faster_whisper_medium_required": self.faster_whisper_medium_required,
            "runtime_model_cache_required": self.runtime_model_cache_required,
            "owner_identity_required": self.owner_identity_required,
            "transcript_state_required": self.transcript_state_required,
            "voice_reply_required": self.voice_reply_required,
            "visible_status_required": self.visible_status_required,
            "explicit_stop_required": self.explicit_stop_required,
            "local_only_required": self.local_only_required,
            "physical_mic_kill_switch_supported": self.physical_mic_kill_switch_supported,
            "hidden_recording_allowed": self.hidden_recording_allowed,
            "cloud_stt_allowed": self.cloud_stt_allowed,
            "remote_stream_allowed": self.remote_stream_allowed,
            "pc_control_allowed": self.pc_control_allowed,
            "mouse_control_allowed": self.mouse_control_allowed,
            "keyboard_control_allowed": self.keyboard_control_allowed,
            "browser_control_allowed": self.browser_control_allowed,
            "app_launch_allowed": self.app_launch_allowed,
            "network_listener_allowed": self.network_listener_allowed,
            "autonomous_action_allowed": self.autonomous_action_allowed,
        }


def build_jarvis_live_conversation_loop_contract() -> (
    JarvisLiveConversationLoopContract
):
    return JarvisLiveConversationLoopContract()


def _require_non_empty(value: str, field_name: str) -> None:
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f"{field_name} must be a non-empty string")


def _require_true(value: bool, field_name: str) -> None:
    if value is not True:
        raise ValueError(f"{field_name} must remain enabled")


def _require_false(value: bool, field_name: str) -> None:
    if value is not False:
        raise ValueError(f"{field_name} must remain disabled")

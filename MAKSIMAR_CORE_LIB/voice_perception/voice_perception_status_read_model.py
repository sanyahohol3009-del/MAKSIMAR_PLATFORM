from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from ANDROID_SHELL.voice_adapter.android_voice_state_bridge import (
    build_android_voice_state_bridge,
)
from IOS_SHELL.voice_adapter.ios_voice_state_bridge import (
    build_ios_voice_state_bridge,
)
from MAKSIMAR_CORE_LIB.voice_perception.asr_backend_adapter_contract import (
    build_asr_backend_adapter_contract,
)
from MAKSIMAR_CORE_LIB.voice_perception.gesture_backend_adapter_contract import (
    build_gesture_backend_adapter_contract,
)
from MAKSIMAR_CORE_LIB.voice_perception.perception_policy_contract import (
    build_perception_policy_contract,
)
from MAKSIMAR_CORE_LIB.voice_perception.voice_clone_backend_adapter_contract import (
    build_voice_clone_backend_adapter_contract,
)


def _require_non_empty(value: str, field_name: str) -> None:
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f"{field_name} must be a non-empty string")


def _require_true(value: bool, field_name: str) -> None:
    if value is not True:
        raise ValueError(f"{field_name} must remain enabled")


def _require_false(value: bool, field_name: str) -> None:
    if value is not False:
        raise ValueError(f"{field_name} must remain disabled")


@dataclass(frozen=True, slots=True)
class VoicePerceptionStatusReadModel:
    phase_id: str
    batch_id: str
    voice_perception_ready_model: bool
    asr_contract_present: bool
    voice_clone_contract_present: bool
    gesture_contract_present: bool
    perception_policy_present: bool
    android_voice_bridge_present: bool
    ios_voice_bridge_present: bool
    owner_voice_gate_required: bool
    raw_audio_blocked_by_default: bool
    text_intent_only: bool
    voice_message_allowed_as_chat_attachment: bool
    voice_message_not_command_without_intent: bool
    shell_execution_allowed: bool
    canonical_write_allowed: bool
    pc_control_allowed: bool
    direct_mobile_control_allowed: bool
    action_execution_allowed: bool
    microphone_runtime_started: bool
    camera_runtime_started: bool
    audio_playback_runtime_started: bool
    model_download_allowed: bool
    junior_model_runtime_enabled: bool
    local_inference_allowed: bool
    windows_voice_edge_parked: bool
    push_to_talk_stt_live_parked: bool
    proposal_only: bool
    read_only: bool

    def __post_init__(self) -> None:
        _require_non_empty(self.phase_id, "phase_id")
        _require_non_empty(self.batch_id, "batch_id")
        if self.phase_id != "PHASE_8":
            raise ValueError("phase_id must remain PHASE_8")
        if self.batch_id != "8.3":
            raise ValueError("batch_id must remain 8.3")
        _require_true(self.voice_perception_ready_model, "voice_perception_ready_model")
        _require_true(self.asr_contract_present, "asr_contract_present")
        _require_true(self.voice_clone_contract_present, "voice_clone_contract_present")
        _require_true(self.gesture_contract_present, "gesture_contract_present")
        _require_true(self.perception_policy_present, "perception_policy_present")
        _require_true(self.android_voice_bridge_present, "android_voice_bridge_present")
        _require_true(self.ios_voice_bridge_present, "ios_voice_bridge_present")
        _require_true(self.owner_voice_gate_required, "owner_voice_gate_required")
        _require_true(self.raw_audio_blocked_by_default, "raw_audio_blocked_by_default")
        _require_true(self.text_intent_only, "text_intent_only")
        _require_true(
            self.voice_message_allowed_as_chat_attachment,
            "voice_message_allowed_as_chat_attachment",
        )
        _require_true(
            self.voice_message_not_command_without_intent,
            "voice_message_not_command_without_intent",
        )
        _require_false(self.shell_execution_allowed, "shell_execution_allowed")
        _require_false(self.canonical_write_allowed, "canonical_write_allowed")
        _require_false(self.pc_control_allowed, "pc_control_allowed")
        _require_false(
            self.direct_mobile_control_allowed,
            "direct_mobile_control_allowed",
        )
        _require_false(self.action_execution_allowed, "action_execution_allowed")
        _require_false(self.microphone_runtime_started, "microphone_runtime_started")
        _require_false(self.camera_runtime_started, "camera_runtime_started")
        _require_false(
            self.audio_playback_runtime_started,
            "audio_playback_runtime_started",
        )
        _require_false(self.model_download_allowed, "model_download_allowed")
        _require_false(
            self.junior_model_runtime_enabled,
            "junior_model_runtime_enabled",
        )
        _require_false(self.local_inference_allowed, "local_inference_allowed")
        _require_true(self.windows_voice_edge_parked, "windows_voice_edge_parked")
        _require_true(
            self.push_to_talk_stt_live_parked,
            "push_to_talk_stt_live_parked",
        )
        _require_true(self.proposal_only, "proposal_only")
        _require_true(self.read_only, "read_only")

    def to_read_model(self) -> dict[str, Any]:
        return {
            "phase_id": self.phase_id,
            "batch_id": self.batch_id,
            "voice_perception_ready_model": self.voice_perception_ready_model,
            "asr_contract_present": self.asr_contract_present,
            "voice_clone_contract_present": self.voice_clone_contract_present,
            "gesture_contract_present": self.gesture_contract_present,
            "perception_policy_present": self.perception_policy_present,
            "android_voice_bridge_present": self.android_voice_bridge_present,
            "ios_voice_bridge_present": self.ios_voice_bridge_present,
            "owner_voice_gate_required": self.owner_voice_gate_required,
            "raw_audio_blocked_by_default": self.raw_audio_blocked_by_default,
            "text_intent_only": self.text_intent_only,
            "voice_message_allowed_as_chat_attachment": (
                self.voice_message_allowed_as_chat_attachment
            ),
            "voice_message_not_command_without_intent": (
                self.voice_message_not_command_without_intent
            ),
            "shell_execution_allowed": self.shell_execution_allowed,
            "canonical_write_allowed": self.canonical_write_allowed,
            "pc_control_allowed": self.pc_control_allowed,
            "direct_mobile_control_allowed": self.direct_mobile_control_allowed,
            "action_execution_allowed": self.action_execution_allowed,
            "microphone_runtime_started": self.microphone_runtime_started,
            "camera_runtime_started": self.camera_runtime_started,
            "audio_playback_runtime_started": self.audio_playback_runtime_started,
            "model_download_allowed": self.model_download_allowed,
            "junior_model_runtime_enabled": self.junior_model_runtime_enabled,
            "local_inference_allowed": self.local_inference_allowed,
            "windows_voice_edge_parked": self.windows_voice_edge_parked,
            "push_to_talk_stt_live_parked": self.push_to_talk_stt_live_parked,
            "proposal_only": self.proposal_only,
            "read_only": self.read_only,
        }


def build_voice_perception_status_read_model() -> VoicePerceptionStatusReadModel:
    asr_contract = build_asr_backend_adapter_contract().to_read_model()
    voice_clone_contract = build_voice_clone_backend_adapter_contract().to_read_model()
    gesture_contract = build_gesture_backend_adapter_contract().to_read_model()
    perception_policy = build_perception_policy_contract().to_read_model()
    android_bridge = build_android_voice_state_bridge().to_read_model()
    ios_bridge = build_ios_voice_state_bridge().to_read_model()

    return VoicePerceptionStatusReadModel(
        phase_id="PHASE_8",
        batch_id="8.3",
        voice_perception_ready_model=True,
        asr_contract_present=bool(asr_contract["proposal_only"]),
        voice_clone_contract_present=bool(voice_clone_contract["proposal_only"]),
        gesture_contract_present=bool(gesture_contract["proposal_only"]),
        perception_policy_present=bool(perception_policy["proposal_only"]),
        android_voice_bridge_present=bool(android_bridge["proposal_only"]),
        ios_voice_bridge_present=bool(ios_bridge["proposal_only"]),
        owner_voice_gate_required=bool(perception_policy["owner_voice_gate_required"]),
        raw_audio_blocked_by_default=bool(
            perception_policy["raw_audio_blocked_by_default"]
            and android_bridge["raw_audio_stream_blocked_by_default"]
            and ios_bridge["raw_audio_stream_blocked_by_default"]
        ),
        text_intent_only=bool(perception_policy["text_intent_only"]),
        voice_message_allowed_as_chat_attachment=True,
        voice_message_not_command_without_intent=True,
        shell_execution_allowed=False,
        canonical_write_allowed=False,
        pc_control_allowed=False,
        direct_mobile_control_allowed=False,
        action_execution_allowed=False,
        microphone_runtime_started=False,
        camera_runtime_started=False,
        audio_playback_runtime_started=False,
        model_download_allowed=False,
        junior_model_runtime_enabled=False,
        local_inference_allowed=False,
        windows_voice_edge_parked=bool(
            perception_policy["WINDOWS_VOICE_EDGE_PARKED"]
        ),
        push_to_talk_stt_live_parked=bool(
            perception_policy["PUSH_TO_TALK_STT_LIVE_PARKED"]
        ),
        proposal_only=True,
        read_only=True,
    )

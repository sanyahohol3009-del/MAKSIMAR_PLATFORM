from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from IOS_SHELL.voice_adapter.mediapipe_ios_adapter_contract import (
    MediaPipeIOSAdapterContract,
)
from IOS_SHELL.voice_adapter.moonshine_ios_adapter_contract import (
    MoonshineIOSAdapterContract,
)


def _require_non_empty(value: str, field_name: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f"{field_name} must be a non-empty string")
    return value.strip()


def _require_true(value: bool, field_name: str) -> None:
    if value is not True:
        raise ValueError(f"{field_name} must remain enabled")


def _require_false(value: bool, field_name: str) -> None:
    if value is not False:
        raise ValueError(f"{field_name} must remain disabled")


@dataclass(frozen=True, slots=True)
class IOSVoiceStateBridge:
    bridge_id: str
    device_id: str
    ios_bundle_id: str
    asr_adapter_ref: str
    gesture_adapter_ref: str
    sends_text_only: bool
    raw_audio_stream_blocked_by_default: bool
    raw_audio_upload_allowed: bool
    raw_audio_persistence_allowed: bool
    command_execution_allowed: bool
    mobile_action_execution_allowed: bool
    direct_phone_control_allowed: bool
    local_inference_allowed: bool
    junior_model_runtime_enabled: bool
    senior_junior_awareness_reference_allowed: bool
    senior_node_role: str
    junior_node_role: str
    phase_9_junior_model_parked: bool
    owner_voice_gate_required: bool
    approval_required_for_actions: bool
    proposal_only: bool

    def __post_init__(self) -> None:
        self_fields = (
            "bridge_id",
            "device_id",
            "ios_bundle_id",
            "asr_adapter_ref",
            "gesture_adapter_ref",
            "senior_node_role",
            "junior_node_role",
        )
        for field_name in self_fields:
            object.__setattr__(
                self,
                field_name,
                _require_non_empty(getattr(self, field_name), field_name),
            )

        _require_true(self.sends_text_only, "sends_text_only")
        _require_true(
            self.raw_audio_stream_blocked_by_default,
            "raw_audio_stream_blocked_by_default",
        )
        _require_false(self.raw_audio_upload_allowed, "raw_audio_upload_allowed")
        _require_false(
            self.raw_audio_persistence_allowed,
            "raw_audio_persistence_allowed",
        )
        _require_false(self.command_execution_allowed, "command_execution_allowed")
        _require_false(
            self.mobile_action_execution_allowed,
            "mobile_action_execution_allowed",
        )
        _require_false(
            self.direct_phone_control_allowed,
            "direct_phone_control_allowed",
        )
        _require_false(self.local_inference_allowed, "local_inference_allowed")
        _require_false(
            self.junior_model_runtime_enabled,
            "junior_model_runtime_enabled",
        )
        _require_true(
            self.senior_junior_awareness_reference_allowed,
            "senior_junior_awareness_reference_allowed",
        )
        if self.senior_node_role != "server_jARVIS_senior":
            raise ValueError("senior_node_role must remain server_jARVIS_senior")
        if self.junior_node_role != "future_mobile_junior":
            raise ValueError("junior_node_role must remain future_mobile_junior")
        _require_true(
            self.phase_9_junior_model_parked,
            "phase_9_junior_model_parked",
        )
        _require_true(self.owner_voice_gate_required, "owner_voice_gate_required")
        _require_true(
            self.approval_required_for_actions,
            "approval_required_for_actions",
        )
        _require_true(self.proposal_only, "proposal_only")

    @classmethod
    def from_adapter_contracts(
        cls,
        *,
        bridge_id: str,
        device_id: str,
        ios_bundle_id: str,
        asr_adapter: MoonshineIOSAdapterContract,
        gesture_adapter: MediaPipeIOSAdapterContract,
    ) -> "IOSVoiceStateBridge":
        if not isinstance(asr_adapter, MoonshineIOSAdapterContract):
            raise ValueError("asr_adapter must be MoonshineIOSAdapterContract")
        if not isinstance(gesture_adapter, MediaPipeIOSAdapterContract):
            raise ValueError("gesture_adapter must be MediaPipeIOSAdapterContract")
        return cls(
            bridge_id=bridge_id,
            device_id=device_id,
            ios_bundle_id=ios_bundle_id,
            asr_adapter_ref=f"ref://{asr_adapter.contract_id}",
            gesture_adapter_ref=f"ref://{gesture_adapter.contract_id}",
            sends_text_only=True,
            raw_audio_stream_blocked_by_default=True,
            raw_audio_upload_allowed=False,
            raw_audio_persistence_allowed=False,
            command_execution_allowed=False,
            mobile_action_execution_allowed=False,
            direct_phone_control_allowed=False,
            local_inference_allowed=False,
            junior_model_runtime_enabled=False,
            senior_junior_awareness_reference_allowed=True,
            senior_node_role="server_jARVIS_senior",
            junior_node_role="future_mobile_junior",
            phase_9_junior_model_parked=True,
            owner_voice_gate_required=True,
            approval_required_for_actions=True,
            proposal_only=True,
        )

    def to_read_model(self) -> dict[str, Any]:
        return {
            "bridge_id": self.bridge_id,
            "device_id": self.device_id,
            "ios_bundle_id": self.ios_bundle_id,
            "asr_adapter_ref": self.asr_adapter_ref,
            "gesture_adapter_ref": self.gesture_adapter_ref,
            "sends_text_only": self.sends_text_only,
            "raw_audio_stream_blocked_by_default": self.raw_audio_stream_blocked_by_default,
            "raw_audio_upload_allowed": self.raw_audio_upload_allowed,
            "raw_audio_persistence_allowed": self.raw_audio_persistence_allowed,
            "command_execution_allowed": self.command_execution_allowed,
            "mobile_action_execution_allowed": self.mobile_action_execution_allowed,
            "direct_phone_control_allowed": self.direct_phone_control_allowed,
            "local_inference_allowed": self.local_inference_allowed,
            "junior_model_runtime_enabled": self.junior_model_runtime_enabled,
            "senior_junior_awareness_reference_allowed": (
                self.senior_junior_awareness_reference_allowed
            ),
            "senior_node_role": self.senior_node_role,
            "junior_node_role": self.junior_node_role,
            "phase_9_junior_model_parked": self.phase_9_junior_model_parked,
            "owner_voice_gate_required": self.owner_voice_gate_required,
            "approval_required_for_actions": self.approval_required_for_actions,
            "proposal_only": self.proposal_only,
        }


def build_ios_voice_state_bridge() -> IOSVoiceStateBridge:
    return IOSVoiceStateBridge.from_adapter_contracts(
        bridge_id="ios_voice_state_bridge_v0_1",
        device_id="ios_voice_device_primary",
        ios_bundle_id="com.maksimar.ios.shell",
        asr_adapter=MoonshineIOSAdapterContract(
            contract_id="moonshine_ios_adapter_contract_v0_1",
            adapter_kind="moonshine_ios_local_asr_candidate",
        ),
        gesture_adapter=MediaPipeIOSAdapterContract(
            contract_id="mediapipe_ios_adapter_contract_v0_1",
            adapter_kind="mediapipe_ios_gesture_candidate",
        ),
    )

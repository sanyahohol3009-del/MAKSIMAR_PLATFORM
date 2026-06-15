from __future__ import annotations

from dataclasses import dataclass
from typing import Any


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
class MediaPipeIOSAdapterContract:
    contract_id: str
    adapter_kind: str
    gesture_candidate_metadata_only: bool = True
    gesture_to_text_intent_only: bool = True
    raw_camera_stream_allowed: bool = False
    raw_audio_stream_allowed: bool = False
    direct_action_allowed: bool = False
    direct_mobile_control_allowed: bool = False
    pc_control_allowed: bool = False
    shell_execution_allowed: bool = False
    canonical_write_allowed: bool = False
    runtime_mutation_allowed: bool = False
    action_execution_allowed: bool = False
    proposal_only: bool = True

    def __post_init__(self) -> None:
        _require_non_empty(self.contract_id, "contract_id")
        _require_non_empty(self.adapter_kind, "adapter_kind")
        _require_true(
            self.gesture_candidate_metadata_only,
            "gesture_candidate_metadata_only",
        )
        _require_true(self.gesture_to_text_intent_only, "gesture_to_text_intent_only")
        _require_false(self.raw_camera_stream_allowed, "raw_camera_stream_allowed")
        _require_false(self.raw_audio_stream_allowed, "raw_audio_stream_allowed")
        _require_false(self.direct_action_allowed, "direct_action_allowed")
        _require_false(
            self.direct_mobile_control_allowed,
            "direct_mobile_control_allowed",
        )
        _require_false(self.pc_control_allowed, "pc_control_allowed")
        _require_false(self.shell_execution_allowed, "shell_execution_allowed")
        _require_false(self.canonical_write_allowed, "canonical_write_allowed")
        _require_false(self.runtime_mutation_allowed, "runtime_mutation_allowed")
        _require_false(self.action_execution_allowed, "action_execution_allowed")
        _require_true(self.proposal_only, "proposal_only")

    def to_read_model(self) -> dict[str, Any]:
        return {
            "contract_id": self.contract_id,
            "adapter_kind": self.adapter_kind,
            "gesture_candidate_metadata_only": self.gesture_candidate_metadata_only,
            "gesture_to_text_intent_only": self.gesture_to_text_intent_only,
            "raw_camera_stream_allowed": self.raw_camera_stream_allowed,
            "raw_audio_stream_allowed": self.raw_audio_stream_allowed,
            "direct_action_allowed": self.direct_action_allowed,
            "direct_mobile_control_allowed": self.direct_mobile_control_allowed,
            "pc_control_allowed": self.pc_control_allowed,
            "shell_execution_allowed": self.shell_execution_allowed,
            "canonical_write_allowed": self.canonical_write_allowed,
            "runtime_mutation_allowed": self.runtime_mutation_allowed,
            "action_execution_allowed": self.action_execution_allowed,
            "proposal_only": self.proposal_only,
        }


def build_mediapipe_ios_adapter_contract() -> MediaPipeIOSAdapterContract:
    return MediaPipeIOSAdapterContract(
        contract_id="mediapipe_ios_adapter_contract_v0_1",
        adapter_kind="mediapipe_ios_gesture_candidate",
    )

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
class PerceptionPolicyContract:
    contract_id: str
    owner_voice_gate_required: bool = True
    raw_audio_blocked_by_default: bool = True
    voice_ownership_still_required: bool = True
    text_intent_only: bool = True
    action_execution_allowed: bool = False
    approval_required_for_actions: bool = True
    proposal_only: bool = True
    shell_execution_allowed: bool = False
    canonical_write_allowed: bool = False
    pc_control_allowed: bool = False
    direct_mobile_control_allowed: bool = False
    junior_mobile_runtime_enabled: bool = False
    local_mobile_model_enabled: bool = False
    local_inference_allowed: bool = False
    senior_junior_awareness_reference_allowed: bool = True
    senior_junior_sync_authority: bool = False
    PHASE_9_JUNIOR_MODEL_PARKED: bool = True
    WINDOWS_VOICE_EDGE_PARKED: bool = True
    PUSH_TO_TALK_STT_LIVE_PARKED: bool = True
    unauthenticated_voice_may_execute_actions: bool = False
    child_family_mobile_voices_may_bypass_approval: bool = False

    def __post_init__(self) -> None:
        _require_non_empty(self.contract_id, "contract_id")
        _require_true(self.owner_voice_gate_required, "owner_voice_gate_required")
        _require_true(self.raw_audio_blocked_by_default, "raw_audio_blocked_by_default")
        _require_true(
            self.voice_ownership_still_required,
            "voice_ownership_still_required",
        )
        _require_true(self.text_intent_only, "text_intent_only")
        _require_false(self.action_execution_allowed, "action_execution_allowed")
        _require_true(
            self.approval_required_for_actions,
            "approval_required_for_actions",
        )
        _require_true(self.proposal_only, "proposal_only")
        _require_false(self.shell_execution_allowed, "shell_execution_allowed")
        _require_false(self.canonical_write_allowed, "canonical_write_allowed")
        _require_false(self.pc_control_allowed, "pc_control_allowed")
        _require_false(
            self.direct_mobile_control_allowed,
            "direct_mobile_control_allowed",
        )
        _require_false(
            self.junior_mobile_runtime_enabled,
            "junior_mobile_runtime_enabled",
        )
        _require_false(self.local_mobile_model_enabled, "local_mobile_model_enabled")
        _require_false(self.local_inference_allowed, "local_inference_allowed")
        _require_true(
            self.senior_junior_awareness_reference_allowed,
            "senior_junior_awareness_reference_allowed",
        )
        _require_false(
            self.senior_junior_sync_authority,
            "senior_junior_sync_authority",
        )
        _require_true(
            self.PHASE_9_JUNIOR_MODEL_PARKED,
            "PHASE_9_JUNIOR_MODEL_PARKED",
        )
        _require_true(self.WINDOWS_VOICE_EDGE_PARKED, "WINDOWS_VOICE_EDGE_PARKED")
        _require_true(
            self.PUSH_TO_TALK_STT_LIVE_PARKED,
            "PUSH_TO_TALK_STT_LIVE_PARKED",
        )
        _require_false(
            self.unauthenticated_voice_may_execute_actions,
            "unauthenticated_voice_may_execute_actions",
        )
        _require_false(
            self.child_family_mobile_voices_may_bypass_approval,
            "child_family_mobile_voices_may_bypass_approval",
        )

    def to_read_model(self) -> dict[str, Any]:
        return {
            "contract_id": self.contract_id,
            "owner_voice_gate_required": self.owner_voice_gate_required,
            "raw_audio_blocked_by_default": self.raw_audio_blocked_by_default,
            "voice_ownership_still_required": self.voice_ownership_still_required,
            "text_intent_only": self.text_intent_only,
            "action_execution_allowed": self.action_execution_allowed,
            "approval_required_for_actions": self.approval_required_for_actions,
            "proposal_only": self.proposal_only,
            "shell_execution_allowed": self.shell_execution_allowed,
            "canonical_write_allowed": self.canonical_write_allowed,
            "pc_control_allowed": self.pc_control_allowed,
            "direct_mobile_control_allowed": self.direct_mobile_control_allowed,
            "junior_mobile_runtime_enabled": self.junior_mobile_runtime_enabled,
            "local_mobile_model_enabled": self.local_mobile_model_enabled,
            "local_inference_allowed": self.local_inference_allowed,
            "senior_junior_awareness_reference_allowed": (
                self.senior_junior_awareness_reference_allowed
            ),
            "senior_junior_sync_authority": self.senior_junior_sync_authority,
            "PHASE_9_JUNIOR_MODEL_PARKED": self.PHASE_9_JUNIOR_MODEL_PARKED,
            "WINDOWS_VOICE_EDGE_PARKED": self.WINDOWS_VOICE_EDGE_PARKED,
            "PUSH_TO_TALK_STT_LIVE_PARKED": self.PUSH_TO_TALK_STT_LIVE_PARKED,
            "unauthenticated_voice_may_execute_actions": (
                self.unauthenticated_voice_may_execute_actions
            ),
            "child_family_mobile_voices_may_bypass_approval": (
                self.child_family_mobile_voices_may_bypass_approval
            ),
        }


def build_perception_policy_contract() -> PerceptionPolicyContract:
    return PerceptionPolicyContract(
        contract_id="perception_policy_contract_v0_1",
    )

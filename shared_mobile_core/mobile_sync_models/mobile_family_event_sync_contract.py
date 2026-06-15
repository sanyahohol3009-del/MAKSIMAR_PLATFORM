from __future__ import annotations

from dataclasses import dataclass
from typing import Any


def _ensure_non_empty(value: str, field_name: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f"{field_name} must be a non-empty string")
    return value.strip()


def _require_true(value: bool, field_name: str) -> None:
    if value is not True:
        raise ValueError(f"{field_name} must be True")


def _require_false(value: bool, field_name: str) -> None:
    if value is not False:
        raise ValueError(f"{field_name} must be False")


@dataclass(frozen=True)
class MobileFamilyEventSyncContract:
    contract_id: str
    mobile_family_event_sync_allowed: bool
    family_event_is_context_only: bool
    family_event_may_create_intent_candidate: bool
    family_event_may_execute_actions: bool
    family_event_may_write_canonical_memory: bool
    family_event_may_control_phone: bool
    family_event_may_control_pc: bool
    owner_family_voice_gate_reference_allowed: bool
    child_voice_may_not_bypass_approval: bool
    server_review_required: bool
    proposal_only: bool

    def __post_init__(self) -> None:
        object.__setattr__(self, "contract_id", _ensure_non_empty(self.contract_id, "contract_id"))
        for field_name in (
            "mobile_family_event_sync_allowed",
            "family_event_is_context_only",
            "family_event_may_create_intent_candidate",
            "owner_family_voice_gate_reference_allowed",
            "child_voice_may_not_bypass_approval",
            "server_review_required",
            "proposal_only",
        ):
            _require_true(getattr(self, field_name), field_name)
        for field_name in (
            "family_event_may_execute_actions",
            "family_event_may_write_canonical_memory",
            "family_event_may_control_phone",
            "family_event_may_control_pc",
        ):
            _require_false(getattr(self, field_name), field_name)

    def to_read_model(self) -> dict[str, Any]:
        return {
            "contract_id": self.contract_id,
            "mobile_family_event_sync_allowed": self.mobile_family_event_sync_allowed,
            "family_event_is_context_only": self.family_event_is_context_only,
            "family_event_may_create_intent_candidate": self.family_event_may_create_intent_candidate,
            "family_event_may_execute_actions": self.family_event_may_execute_actions,
            "family_event_may_write_canonical_memory": self.family_event_may_write_canonical_memory,
            "family_event_may_control_phone": self.family_event_may_control_phone,
            "family_event_may_control_pc": self.family_event_may_control_pc,
            "owner_family_voice_gate_reference_allowed": self.owner_family_voice_gate_reference_allowed,
            "child_voice_may_not_bypass_approval": self.child_voice_may_not_bypass_approval,
            "server_review_required": self.server_review_required,
            "proposal_only": self.proposal_only,
        }


def build_mobile_family_event_sync_contract() -> MobileFamilyEventSyncContract:
    return MobileFamilyEventSyncContract(
        contract_id="mobile_family_event_sync_contract_v0_1",
        mobile_family_event_sync_allowed=True,
        family_event_is_context_only=True,
        family_event_may_create_intent_candidate=True,
        family_event_may_execute_actions=False,
        family_event_may_write_canonical_memory=False,
        family_event_may_control_phone=False,
        family_event_may_control_pc=False,
        owner_family_voice_gate_reference_allowed=True,
        child_voice_may_not_bypass_approval=True,
        server_review_required=True,
        proposal_only=True,
    )

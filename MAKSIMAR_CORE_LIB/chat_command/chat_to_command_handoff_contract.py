from __future__ import annotations

from dataclasses import dataclass
from typing import Tuple


_ALLOWED_SOURCE_CHANNELS = ("chat_message", "dashboard_button", "voice_handoff", "mobile_handoff")
_ALLOWED_HANDOFF_STATES = ("declared", "policy_review_required", "approval_required", "blocked", "ready_for_control_plane")
_ALLOWED_CONTROL_PLANE_TARGETS = ("proposal_engine", "policy_gate", "approval_gate", "sandbox_planner")


def _ensure_non_empty(value: str, field_name: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f"{field_name} must be a non-empty string")
    return value.strip()


def _ensure_allowed(value: str, field_name: str, allowed: Tuple[str, ...]) -> str:
    value = _ensure_non_empty(value, field_name)
    if value not in allowed:
        raise ValueError(f"{field_name} must be one of {allowed}: {value}")
    return value


@dataclass(frozen=True)
class ChatToCommandHandoffContract:
    """Canonical chat-to-command handoff contract.

    Contract only. It converts a chat-origin intent into a controlled handoff
    envelope. It does not execute commands, mutate runtime, call OpenIM, call
    mobile APIs, or bypass policy/approval/sandbox gates.
    """

    handoff_id: str
    source_message_id: str
    source_room_id: str
    source_identity_id: str
    source_channel: str
    normalized_intent: str
    control_plane_target: str
    handoff_state: str
    policy_review_required: bool
    operator_approval_required: bool
    sandbox_required: bool
    direct_execution_allowed: bool
    runtime_mutation_allowed: bool
    external_adapter_execution_allowed: bool

    def __post_init__(self) -> None:
        object.__setattr__(self, "handoff_id", _ensure_non_empty(self.handoff_id, "handoff_id"))
        object.__setattr__(self, "source_message_id", _ensure_non_empty(self.source_message_id, "source_message_id"))
        object.__setattr__(self, "source_room_id", _ensure_non_empty(self.source_room_id, "source_room_id"))
        object.__setattr__(self, "source_identity_id", _ensure_non_empty(self.source_identity_id, "source_identity_id"))
        object.__setattr__(self, "source_channel", _ensure_allowed(self.source_channel, "source_channel", _ALLOWED_SOURCE_CHANNELS))
        object.__setattr__(self, "normalized_intent", _ensure_non_empty(self.normalized_intent, "normalized_intent"))
        object.__setattr__(
            self,
            "control_plane_target",
            _ensure_allowed(self.control_plane_target, "control_plane_target", _ALLOWED_CONTROL_PLANE_TARGETS),
        )
        object.__setattr__(self, "handoff_state", _ensure_allowed(self.handoff_state, "handoff_state", _ALLOWED_HANDOFF_STATES))

        if not self.policy_review_required:
            raise ValueError("policy_review_required must be True")
        if not self.operator_approval_required:
            raise ValueError("operator_approval_required must be True")
        if not self.sandbox_required:
            raise ValueError("sandbox_required must be True")
        if self.direct_execution_allowed:
            raise ValueError("direct_execution_allowed must be False")
        if self.runtime_mutation_allowed:
            raise ValueError("runtime_mutation_allowed must be False")
        if self.external_adapter_execution_allowed:
            raise ValueError("external_adapter_execution_allowed must be False")

        if self.handoff_state == "ready_for_control_plane" and self.control_plane_target == "approval_gate":
            raise ValueError("ready_for_control_plane must target proposal_engine, policy_gate, or sandbox_planner first")

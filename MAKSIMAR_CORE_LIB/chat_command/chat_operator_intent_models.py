from __future__ import annotations

from dataclasses import dataclass
from typing import Tuple


_ALLOWED_SOURCE_SURFACES = ("chat_dashboard", "mobile_chat", "voice_handoff", "operator_button")
_ALLOWED_RISK_LEVELS = ("low", "medium", "high", "blocked")
_ALLOWED_INTENT_STATES = ("review_required", "approval_required", "blocked", "ready_for_control_plane")


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
class ChatOperatorIntentModel:
    intent_id: str
    source_message_id: str
    source_surface: str
    normalized_intent: str
    intent_state: str
    risk_level: str
    policy_review_required: bool
    operator_approval_required: bool
    control_plane_handoff_required: bool
    sandbox_required: bool
    direct_execution_allowed: bool
    runtime_mutation_allowed: bool

    def __post_init__(self) -> None:
        object.__setattr__(self, "intent_id", _ensure_non_empty(self.intent_id, "intent_id"))
        object.__setattr__(self, "source_message_id", _ensure_non_empty(self.source_message_id, "source_message_id"))
        object.__setattr__(
            self,
            "source_surface",
            _ensure_allowed(self.source_surface, "source_surface", _ALLOWED_SOURCE_SURFACES),
        )
        object.__setattr__(self, "normalized_intent", _ensure_non_empty(self.normalized_intent, "normalized_intent"))
        object.__setattr__(self, "intent_state", _ensure_allowed(self.intent_state, "intent_state", _ALLOWED_INTENT_STATES))
        object.__setattr__(self, "risk_level", _ensure_allowed(self.risk_level, "risk_level", _ALLOWED_RISK_LEVELS))

        if not self.policy_review_required:
            raise ValueError("policy_review_required must be True")
        if not self.operator_approval_required:
            raise ValueError("operator_approval_required must be True")
        if not self.control_plane_handoff_required:
            raise ValueError("control_plane_handoff_required must be True")
        if not self.sandbox_required:
            raise ValueError("sandbox_required must be True")
        if self.direct_execution_allowed:
            raise ValueError("direct_execution_allowed must be False")
        if self.runtime_mutation_allowed:
            raise ValueError("runtime_mutation_allowed must be False")
        if self.risk_level == "blocked" and self.intent_state != "blocked":
            raise ValueError("blocked risk_level requires intent_state='blocked'")

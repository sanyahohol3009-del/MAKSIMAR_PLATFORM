from __future__ import annotations

from dataclasses import dataclass
from typing import Tuple


_ALLOWED_COMMAND_INTENT_KINDS = ("operator_request", "dashboard_button", "voice_handoff", "mobile_handoff")
_ALLOWED_RISK_LEVELS = ("low", "medium", "high", "blocked")


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
class CommandMessageContract:
    """Canonical command-intent message contract.

    A command message is only an intent envelope. It cannot execute directly.
    Execution must go through control-plane, policy, audit, and approval gates.
    """

    command_message_id: str
    source_message_id: str
    source_room_id: str
    source_identity_id: str
    command_intent_kind: str
    normalized_intent: str
    risk_level: str
    control_plane_handoff_required: bool
    operator_approval_required: bool
    direct_execution_allowed: bool
    runtime_mutation_allowed: bool

    def __post_init__(self) -> None:
        object.__setattr__(self, "command_message_id", _ensure_non_empty(self.command_message_id, "command_message_id"))
        object.__setattr__(self, "source_message_id", _ensure_non_empty(self.source_message_id, "source_message_id"))
        object.__setattr__(self, "source_room_id", _ensure_non_empty(self.source_room_id, "source_room_id"))
        object.__setattr__(self, "source_identity_id", _ensure_non_empty(self.source_identity_id, "source_identity_id"))
        object.__setattr__(
            self,
            "command_intent_kind",
            _ensure_allowed(self.command_intent_kind, "command_intent_kind", _ALLOWED_COMMAND_INTENT_KINDS),
        )
        object.__setattr__(self, "normalized_intent", _ensure_non_empty(self.normalized_intent, "normalized_intent"))
        object.__setattr__(self, "risk_level", _ensure_allowed(self.risk_level, "risk_level", _ALLOWED_RISK_LEVELS))

        if not self.control_plane_handoff_required:
            raise ValueError("control_plane_handoff_required must be True")
        if not self.operator_approval_required:
            raise ValueError("operator_approval_required must be True")
        if self.direct_execution_allowed:
            raise ValueError("direct_execution_allowed must be False")
        if self.runtime_mutation_allowed:
            raise ValueError("runtime_mutation_allowed must be False")
        if self.risk_level == "blocked" and self.command_intent_kind != "operator_request":
            raise ValueError("blocked command intents must remain operator_request review items")

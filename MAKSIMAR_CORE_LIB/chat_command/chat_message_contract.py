from __future__ import annotations

from dataclasses import dataclass
from typing import Tuple


_ALLOWED_MESSAGE_KINDS = ("human_text", "jarvis_text", "system_notice", "command_intent", "adapter_event")
_ALLOWED_MESSAGE_STATES = ("draft", "queued", "accepted", "rejected", "delivered", "archived")


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
class ChatMessageContract:
    """Canonical chat message contract.

    Contract only. It does not send, persist, sync, encrypt, or execute a message.
    Attachments and offline delivery are added in BATCH 3.2.
    """

    message_id: str
    room_id: str
    sender_identity_id: str
    message_kind: str
    text_payload: str
    message_state: str
    created_at_utc: str
    direct_execution_allowed: bool
    runtime_mutation_allowed: bool

    def __post_init__(self) -> None:
        object.__setattr__(self, "message_id", _ensure_non_empty(self.message_id, "message_id"))
        object.__setattr__(self, "room_id", _ensure_non_empty(self.room_id, "room_id"))
        object.__setattr__(self, "sender_identity_id", _ensure_non_empty(self.sender_identity_id, "sender_identity_id"))
        object.__setattr__(
            self,
            "message_kind",
            _ensure_allowed(self.message_kind, "message_kind", _ALLOWED_MESSAGE_KINDS),
        )
        object.__setattr__(self, "text_payload", _ensure_non_empty(self.text_payload, "text_payload"))
        object.__setattr__(
            self,
            "message_state",
            _ensure_allowed(self.message_state, "message_state", _ALLOWED_MESSAGE_STATES),
        )
        object.__setattr__(self, "created_at_utc", _ensure_non_empty(self.created_at_utc, "created_at_utc"))

        if self.direct_execution_allowed:
            raise ValueError("direct_execution_allowed must be False for chat message contracts")
        if self.runtime_mutation_allowed:
            raise ValueError("runtime_mutation_allowed must be False for chat message contracts")

        if self.message_kind == "command_intent" and self.message_state == "delivered":
            raise ValueError("command_intent messages must not be delivered as executed commands")

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Tuple


_ALLOWED_EVENT_KINDS = ("session_registered", "message_routed", "offline_queued", "command_review_required", "blocked")


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
class ChatAuditEvent:
    event_id: str
    event_kind: str
    subject_id: str
    actor_identity_id: str
    created_at_utc: str
    policy_checked: bool
    append_only: bool
    direct_execution_allowed: bool
    canonical_write_allowed: bool
    external_network_access_allowed: bool

    def __post_init__(self) -> None:
        object.__setattr__(self, "event_id", _ensure_non_empty(self.event_id, "event_id"))
        object.__setattr__(self, "event_kind", _ensure_allowed(self.event_kind, "event_kind", _ALLOWED_EVENT_KINDS))
        object.__setattr__(self, "subject_id", _ensure_non_empty(self.subject_id, "subject_id"))
        object.__setattr__(self, "actor_identity_id", _ensure_non_empty(self.actor_identity_id, "actor_identity_id"))
        object.__setattr__(self, "created_at_utc", _ensure_non_empty(self.created_at_utc, "created_at_utc"))

        if not self.policy_checked:
            raise ValueError("policy_checked must be True")
        if not self.append_only:
            raise ValueError("append_only must be True")
        if self.direct_execution_allowed:
            raise ValueError("direct_execution_allowed must be False")
        if self.canonical_write_allowed:
            raise ValueError("canonical_write_allowed must be False")
        if self.external_network_access_allowed:
            raise ValueError("external_network_access_allowed must be False")


@dataclass
class ChatAuditRuntime:
    """Append-only in-memory chat audit runtime.

    It is not a canonical audit database. It provides deterministic batch-level
    audit behavior for chat runtime decisions.
    """

    _events: Tuple[ChatAuditEvent, ...] = field(default_factory=tuple)

    def append_event(self, event: ChatAuditEvent) -> ChatAuditEvent:
        self._events = (*self._events, event)
        return event

    def list_events(self) -> Tuple[ChatAuditEvent, ...]:
        return self._events

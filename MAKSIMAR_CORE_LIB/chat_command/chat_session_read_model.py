from __future__ import annotations

from dataclasses import dataclass
from typing import Tuple


_ALLOWED_SESSION_STATES = ("active", "offline", "suspended", "closed")


def _ensure_non_empty(value: str, field_name: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f"{field_name} must be a non-empty string")
    return value.strip()


def _ensure_allowed(value: str, field_name: str, allowed: Tuple[str, ...]) -> str:
    value = _ensure_non_empty(value, field_name)
    if value not in allowed:
        raise ValueError(f"{field_name} must be one of {allowed}: {value}")
    return value


def _ensure_non_negative_int(value: int, field_name: str) -> int:
    if not isinstance(value, int) or value < 0:
        raise ValueError(f"{field_name} must be a non-negative integer")
    return value


@dataclass(frozen=True)
class ChatSessionReadModel:
    read_model_id: str
    session_id: str
    room_id: str
    participant_count: int
    session_state: str
    unread_count: int
    pending_outbound_count: int
    dashboard_read_only: bool
    direct_execution_allowed: bool
    runtime_mutation_allowed: bool
    canonical_truth_write_allowed: bool

    def __post_init__(self) -> None:
        object.__setattr__(self, "read_model_id", _ensure_non_empty(self.read_model_id, "read_model_id"))
        object.__setattr__(self, "session_id", _ensure_non_empty(self.session_id, "session_id"))
        object.__setattr__(self, "room_id", _ensure_non_empty(self.room_id, "room_id"))
        object.__setattr__(self, "participant_count", _ensure_non_negative_int(self.participant_count, "participant_count"))
        object.__setattr__(
            self,
            "session_state",
            _ensure_allowed(self.session_state, "session_state", _ALLOWED_SESSION_STATES),
        )
        object.__setattr__(self, "unread_count", _ensure_non_negative_int(self.unread_count, "unread_count"))
        object.__setattr__(
            self,
            "pending_outbound_count",
            _ensure_non_negative_int(self.pending_outbound_count, "pending_outbound_count"),
        )

        if self.participant_count == 0:
            raise ValueError("participant_count must be greater than zero")
        if not self.dashboard_read_only:
            raise ValueError("dashboard_read_only must be True")
        if self.direct_execution_allowed:
            raise ValueError("direct_execution_allowed must be False")
        if self.runtime_mutation_allowed:
            raise ValueError("runtime_mutation_allowed must be False")
        if self.canonical_truth_write_allowed:
            raise ValueError("canonical_truth_write_allowed must be False")

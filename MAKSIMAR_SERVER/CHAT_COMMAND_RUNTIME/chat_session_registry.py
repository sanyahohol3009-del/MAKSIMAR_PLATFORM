from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict, Tuple


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


def _ensure_participants(values: Tuple[str, ...]) -> Tuple[str, ...]:
    if not isinstance(values, tuple) or not values:
        raise ValueError("participant_identity_ids must be a non-empty tuple")
    normalized = tuple(_ensure_non_empty(value, "participant_identity_id") for value in values)
    if len(set(normalized)) != len(normalized):
        raise ValueError("participant_identity_ids must not contain duplicates")
    return normalized


@dataclass(frozen=True)
class ChatSessionRecord:
    session_id: str
    room_id: str
    participant_identity_ids: Tuple[str, ...]
    session_state: str
    command_execution_allowed: bool
    external_network_access_allowed: bool
    canonical_write_allowed: bool

    def __post_init__(self) -> None:
        object.__setattr__(self, "session_id", _ensure_non_empty(self.session_id, "session_id"))
        object.__setattr__(self, "room_id", _ensure_non_empty(self.room_id, "room_id"))
        object.__setattr__(self, "participant_identity_ids", _ensure_participants(self.participant_identity_ids))
        object.__setattr__(self, "session_state", _ensure_allowed(self.session_state, "session_state", _ALLOWED_SESSION_STATES))

        if self.command_execution_allowed:
            raise ValueError("command_execution_allowed must be False")
        if self.external_network_access_allowed:
            raise ValueError("external_network_access_allowed must be False")
        if self.canonical_write_allowed:
            raise ValueError("canonical_write_allowed must be False")


@dataclass
class ChatSessionRegistry:
    """In-memory server chat session registry.

    Runtime scope is local process memory only. It does not open sockets, create
    external chat rooms, write canonical truth, or execute commands.
    """

    _sessions: Dict[str, ChatSessionRecord] = field(default_factory=dict)

    def register_session(self, record: ChatSessionRecord) -> ChatSessionRecord:
        if record.session_id in self._sessions:
            raise ValueError(f"session already registered: {record.session_id}")
        self._sessions[record.session_id] = record
        return record

    def get_session(self, session_id: str) -> ChatSessionRecord:
        session_id = _ensure_non_empty(session_id, "session_id")
        try:
            return self._sessions[session_id]
        except KeyError as exc:
            raise KeyError(f"unknown chat session: {session_id}") from exc

    def close_session(self, session_id: str) -> ChatSessionRecord:
        current = self.get_session(session_id)
        closed = ChatSessionRecord(
            session_id=current.session_id,
            room_id=current.room_id,
            participant_identity_ids=current.participant_identity_ids,
            session_state="closed",
            command_execution_allowed=False,
            external_network_access_allowed=False,
            canonical_write_allowed=False,
        )
        self._sessions[session_id] = closed
        return closed

    def list_sessions(self) -> Tuple[ChatSessionRecord, ...]:
        return tuple(self._sessions.values())

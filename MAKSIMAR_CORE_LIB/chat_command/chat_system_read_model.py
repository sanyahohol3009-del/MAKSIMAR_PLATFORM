from __future__ import annotations

from dataclasses import dataclass
from typing import Tuple


_ALLOWED_SYSTEM_STATES = ("online_reference", "degraded_reference", "offline_reference", "blocked")


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
class ChatSystemReadModel:
    read_model_id: str
    system_state: str
    active_session_count: int
    queued_message_count: int
    blocked_message_count: int
    file_transfer_count: int
    dashboard_read_only: bool
    direct_execution_allowed: bool
    runtime_mutation_allowed: bool
    canonical_truth_write_allowed: bool

    def __post_init__(self) -> None:
        object.__setattr__(self, "read_model_id", _ensure_non_empty(self.read_model_id, "read_model_id"))
        object.__setattr__(
            self,
            "system_state",
            _ensure_allowed(self.system_state, "system_state", _ALLOWED_SYSTEM_STATES),
        )
        object.__setattr__(
            self,
            "active_session_count",
            _ensure_non_negative_int(self.active_session_count, "active_session_count"),
        )
        object.__setattr__(
            self,
            "queued_message_count",
            _ensure_non_negative_int(self.queued_message_count, "queued_message_count"),
        )
        object.__setattr__(
            self,
            "blocked_message_count",
            _ensure_non_negative_int(self.blocked_message_count, "blocked_message_count"),
        )
        object.__setattr__(
            self,
            "file_transfer_count",
            _ensure_non_negative_int(self.file_transfer_count, "file_transfer_count"),
        )

        if not self.dashboard_read_only:
            raise ValueError("dashboard_read_only must be True")
        if self.direct_execution_allowed:
            raise ValueError("direct_execution_allowed must be False")
        if self.runtime_mutation_allowed:
            raise ValueError("runtime_mutation_allowed must be False")
        if self.canonical_truth_write_allowed:
            raise ValueError("canonical_truth_write_allowed must be False")

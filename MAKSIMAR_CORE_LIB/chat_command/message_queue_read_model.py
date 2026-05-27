from __future__ import annotations

from dataclasses import dataclass
from typing import Tuple


_ALLOWED_QUEUE_STATES = ("empty", "active", "backlog", "blocked")


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
class MessageQueueReadModel:
    read_model_id: str
    queue_state: str
    queued_count: int
    waiting_for_sync_count: int
    blocked_count: int
    oldest_message_age_seconds: int
    dashboard_read_only: bool
    direct_delivery_allowed: bool
    external_network_access_allowed: bool
    runtime_mutation_allowed: bool

    def __post_init__(self) -> None:
        object.__setattr__(self, "read_model_id", _ensure_non_empty(self.read_model_id, "read_model_id"))
        object.__setattr__(self, "queue_state", _ensure_allowed(self.queue_state, "queue_state", _ALLOWED_QUEUE_STATES))
        object.__setattr__(self, "queued_count", _ensure_non_negative_int(self.queued_count, "queued_count"))
        object.__setattr__(
            self,
            "waiting_for_sync_count",
            _ensure_non_negative_int(self.waiting_for_sync_count, "waiting_for_sync_count"),
        )
        object.__setattr__(self, "blocked_count", _ensure_non_negative_int(self.blocked_count, "blocked_count"))
        object.__setattr__(
            self,
            "oldest_message_age_seconds",
            _ensure_non_negative_int(self.oldest_message_age_seconds, "oldest_message_age_seconds"),
        )

        if not self.dashboard_read_only:
            raise ValueError("dashboard_read_only must be True")
        if self.direct_delivery_allowed:
            raise ValueError("direct_delivery_allowed must be False")
        if self.external_network_access_allowed:
            raise ValueError("external_network_access_allowed must be False")
        if self.runtime_mutation_allowed:
            raise ValueError("runtime_mutation_allowed must be False")

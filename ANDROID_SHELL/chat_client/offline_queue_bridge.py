from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict, Tuple


_ALLOWED_QUEUE_STATES = ("queued_local", "waiting_for_server", "delivered_reference", "blocked")


def _ensure_non_empty(value: str, field_name: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f"{field_name} must be a non-empty string")
    return value.strip()


@dataclass(frozen=True)
class AndroidOfflineQueueBridgeEntry:
    delivery_id: str
    message_id: str
    target_room_id: str
    queue_state: str
    bounded_retry_required: bool
    wake_lock_allowed: bool
    direct_mobile_api_execution_allowed: bool
    external_network_access_allowed: bool

    def __post_init__(self) -> None:
        object.__setattr__(self, "delivery_id", _ensure_non_empty(self.delivery_id, "delivery_id"))
        object.__setattr__(self, "message_id", _ensure_non_empty(self.message_id, "message_id"))
        object.__setattr__(self, "target_room_id", _ensure_non_empty(self.target_room_id, "target_room_id"))

        if self.queue_state not in _ALLOWED_QUEUE_STATES:
            raise ValueError(f"queue_state must be one of {_ALLOWED_QUEUE_STATES}: {self.queue_state}")
        if not self.bounded_retry_required:
            raise ValueError("bounded_retry_required must be True")
        if self.wake_lock_allowed:
            raise ValueError("wake_lock_allowed must be False")
        if self.direct_mobile_api_execution_allowed:
            raise ValueError("direct_mobile_api_execution_allowed must be False")
        if self.external_network_access_allowed:
            raise ValueError("external_network_access_allowed must be False")


@dataclass
class AndroidOfflineQueueBridge:
    """In-memory Android offline queue bridge."""

    _entries: Dict[str, AndroidOfflineQueueBridgeEntry] = field(default_factory=dict)

    def enqueue(self, entry: AndroidOfflineQueueBridgeEntry) -> AndroidOfflineQueueBridgeEntry:
        if entry.delivery_id in self._entries:
            raise ValueError(f"delivery already queued: {entry.delivery_id}")
        self._entries[entry.delivery_id] = entry
        return entry

    def mark_waiting_for_server(self, delivery_id: str) -> AndroidOfflineQueueBridgeEntry:
        current = self.get_entry(delivery_id)
        updated = AndroidOfflineQueueBridgeEntry(
            delivery_id=current.delivery_id,
            message_id=current.message_id,
            target_room_id=current.target_room_id,
            queue_state="waiting_for_server",
            bounded_retry_required=True,
            wake_lock_allowed=False,
            direct_mobile_api_execution_allowed=False,
            external_network_access_allowed=False,
        )
        self._entries[delivery_id] = updated
        return updated

    def get_entry(self, delivery_id: str) -> AndroidOfflineQueueBridgeEntry:
        delivery_id = _ensure_non_empty(delivery_id, "delivery_id")
        try:
            return self._entries[delivery_id]
        except KeyError as exc:
            raise KeyError(f"unknown offline delivery: {delivery_id}") from exc

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict, Tuple

from MAKSIMAR_CORE_LIB.chat_command.offline_delivery_contract import OfflineDeliveryContract


_ALLOWED_QUEUE_STATES = ("queued", "delivered_reference", "expired", "blocked")


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
class OfflineQueueEntry:
    delivery_id: str
    message_id: str
    target_device_id: str
    queue_state: str
    wake_device_allowed: bool
    external_network_access_allowed: bool
    direct_mobile_api_execution_allowed: bool

    def __post_init__(self) -> None:
        object.__setattr__(self, "delivery_id", _ensure_non_empty(self.delivery_id, "delivery_id"))
        object.__setattr__(self, "message_id", _ensure_non_empty(self.message_id, "message_id"))
        object.__setattr__(self, "target_device_id", _ensure_non_empty(self.target_device_id, "target_device_id"))
        object.__setattr__(self, "queue_state", _ensure_allowed(self.queue_state, "queue_state", _ALLOWED_QUEUE_STATES))

        if self.wake_device_allowed:
            raise ValueError("wake_device_allowed must be False")
        if self.external_network_access_allowed:
            raise ValueError("external_network_access_allowed must be False")
        if self.direct_mobile_api_execution_allowed:
            raise ValueError("direct_mobile_api_execution_allowed must be False")


@dataclass
class OfflineQueueRuntime:
    """In-memory offline queue.

    It records delivery references only. It does not wake devices, start sync,
    open network connections, or call Android/iOS APIs.
    """

    _entries: Dict[str, OfflineQueueEntry] = field(default_factory=dict)

    def enqueue_delivery(self, delivery: OfflineDeliveryContract) -> OfflineQueueEntry:
        if delivery.delivery_id in self._entries:
            raise ValueError(f"delivery already queued: {delivery.delivery_id}")

        entry = OfflineQueueEntry(
            delivery_id=delivery.delivery_id,
            message_id=delivery.message_id,
            target_device_id=delivery.target_device_id,
            queue_state="queued",
            wake_device_allowed=False,
            external_network_access_allowed=False,
            direct_mobile_api_execution_allowed=False,
        )
        self._entries[entry.delivery_id] = entry
        return entry

    def mark_delivered_reference(self, delivery_id: str) -> OfflineQueueEntry:
        current = self.get_entry(delivery_id)
        delivered = OfflineQueueEntry(
            delivery_id=current.delivery_id,
            message_id=current.message_id,
            target_device_id=current.target_device_id,
            queue_state="delivered_reference",
            wake_device_allowed=False,
            external_network_access_allowed=False,
            direct_mobile_api_execution_allowed=False,
        )
        self._entries[delivery_id] = delivered
        return delivered

    def get_entry(self, delivery_id: str) -> OfflineQueueEntry:
        delivery_id = _ensure_non_empty(delivery_id, "delivery_id")
        try:
            return self._entries[delivery_id]
        except KeyError as exc:
            raise KeyError(f"unknown offline delivery: {delivery_id}") from exc

    def list_entries(self) -> Tuple[OfflineQueueEntry, ...]:
        return tuple(self._entries.values())

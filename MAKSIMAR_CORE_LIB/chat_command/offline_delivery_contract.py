from __future__ import annotations

from dataclasses import dataclass
from typing import Tuple


_ALLOWED_DELIVERY_STATES = ("queued_offline", "waiting_for_sync", "delivered_reference", "expired", "blocked")
_ALLOWED_RETRY_POLICIES = ("none", "bounded")


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
class OfflineDeliveryContract:
    """Canonical offline delivery contract.

    Contract only. It does not send messages, wake mobile devices, start sync,
    open sockets, or mutate runtime queues.
    """

    delivery_id: str
    message_id: str
    target_identity_id: str
    target_device_id: str
    delivery_state: str
    retry_policy: str
    max_retry_count: int
    server_sync_required: bool
    external_network_access_allowed: bool
    direct_mobile_api_execution_allowed: bool
    runtime_mutation_allowed: bool

    def __post_init__(self) -> None:
        object.__setattr__(self, "delivery_id", _ensure_non_empty(self.delivery_id, "delivery_id"))
        object.__setattr__(self, "message_id", _ensure_non_empty(self.message_id, "message_id"))
        object.__setattr__(self, "target_identity_id", _ensure_non_empty(self.target_identity_id, "target_identity_id"))
        object.__setattr__(self, "target_device_id", _ensure_non_empty(self.target_device_id, "target_device_id"))
        object.__setattr__(self, "delivery_state", _ensure_allowed(self.delivery_state, "delivery_state", _ALLOWED_DELIVERY_STATES))
        object.__setattr__(self, "retry_policy", _ensure_allowed(self.retry_policy, "retry_policy", _ALLOWED_RETRY_POLICIES))
        object.__setattr__(self, "max_retry_count", _ensure_non_negative_int(self.max_retry_count, "max_retry_count"))

        if self.retry_policy == "none" and self.max_retry_count != 0:
            raise ValueError("max_retry_count must be 0 when retry_policy is none")
        if self.retry_policy == "bounded" and self.max_retry_count == 0:
            raise ValueError("max_retry_count must be > 0 when retry_policy is bounded")
        if not self.server_sync_required:
            raise ValueError("server_sync_required must be True for offline delivery")
        if self.external_network_access_allowed:
            raise ValueError("external_network_access_allowed must be False")
        if self.direct_mobile_api_execution_allowed:
            raise ValueError("direct_mobile_api_execution_allowed must be False")
        if self.runtime_mutation_allowed:
            raise ValueError("runtime_mutation_allowed must be False")

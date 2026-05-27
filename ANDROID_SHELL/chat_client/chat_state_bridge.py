from __future__ import annotations

from dataclasses import dataclass
from typing import Tuple


_ALLOWED_CONNECTION_STATES = ("offline", "server_available", "p2p_local", "sync_pending")


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
class AndroidChatStateSnapshot:
    bridge_id: str
    device_id: str
    active_room_id: str
    connection_state: str
    unread_count: int
    pending_outbound_count: int
    dashboard_visible: bool
    direct_server_write_allowed: bool
    runtime_execution_allowed: bool
    canonical_truth_write_allowed: bool

    def __post_init__(self) -> None:
        object.__setattr__(self, "bridge_id", _ensure_non_empty(self.bridge_id, "bridge_id"))
        object.__setattr__(self, "device_id", _ensure_non_empty(self.device_id, "device_id"))
        object.__setattr__(self, "active_room_id", _ensure_non_empty(self.active_room_id, "active_room_id"))
        object.__setattr__(
            self,
            "connection_state",
            _ensure_allowed(self.connection_state, "connection_state", _ALLOWED_CONNECTION_STATES),
        )
        object.__setattr__(self, "unread_count", _ensure_non_negative_int(self.unread_count, "unread_count"))
        object.__setattr__(
            self,
            "pending_outbound_count",
            _ensure_non_negative_int(self.pending_outbound_count, "pending_outbound_count"),
        )

        if self.direct_server_write_allowed:
            raise ValueError("direct_server_write_allowed must be False")
        if self.runtime_execution_allowed:
            raise ValueError("runtime_execution_allowed must be False")
        if self.canonical_truth_write_allowed:
            raise ValueError("canonical_truth_write_allowed must be False")


class AndroidChatStateBridge:
    """Read-only Android chat state bridge."""

    def build_snapshot(
        self,
        bridge_id: str,
        device_id: str,
        active_room_id: str,
        connection_state: str,
        unread_count: int,
        pending_outbound_count: int,
    ) -> AndroidChatStateSnapshot:
        return AndroidChatStateSnapshot(
            bridge_id=bridge_id,
            device_id=device_id,
            active_room_id=active_room_id,
            connection_state=connection_state,
            unread_count=unread_count,
            pending_outbound_count=pending_outbound_count,
            dashboard_visible=True,
            direct_server_write_allowed=False,
            runtime_execution_allowed=False,
            canonical_truth_write_allowed=False,
        )

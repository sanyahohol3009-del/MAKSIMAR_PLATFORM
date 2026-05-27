from __future__ import annotations

from dataclasses import dataclass
from typing import Tuple


_ALLOWED_SYNC_MODES = ("manual", "server_available", "offline_only")
_ALLOWED_MESSAGE_SCOPES = ("metadata_only", "message_reference", "attachment_reference")


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
class AndroidChatSyncContract:
    """Android chat sync contract.

    Contract only. It does not call Android APIs, start services, open sockets,
    sync with a server, or mutate canonical truth.
    """

    sync_binding_id: str
    device_id: str
    server_node_id: str
    sync_mode: str
    message_scope: str
    encryption_required: bool
    direct_network_call_allowed: bool
    direct_server_write_allowed: bool
    background_service_start_allowed: bool
    canonical_truth_write_allowed: bool

    def __post_init__(self) -> None:
        object.__setattr__(self, "sync_binding_id", _ensure_non_empty(self.sync_binding_id, "sync_binding_id"))
        object.__setattr__(self, "device_id", _ensure_non_empty(self.device_id, "device_id"))
        object.__setattr__(self, "server_node_id", _ensure_non_empty(self.server_node_id, "server_node_id"))
        object.__setattr__(self, "sync_mode", _ensure_allowed(self.sync_mode, "sync_mode", _ALLOWED_SYNC_MODES))
        object.__setattr__(
            self,
            "message_scope",
            _ensure_allowed(self.message_scope, "message_scope", _ALLOWED_MESSAGE_SCOPES),
        )

        if not self.encryption_required:
            raise ValueError("encryption_required must be True")
        if self.direct_network_call_allowed:
            raise ValueError("direct_network_call_allowed must be False")
        if self.direct_server_write_allowed:
            raise ValueError("direct_server_write_allowed must be False")
        if self.background_service_start_allowed:
            raise ValueError("background_service_start_allowed must be False")
        if self.canonical_truth_write_allowed:
            raise ValueError("canonical_truth_write_allowed must be False")

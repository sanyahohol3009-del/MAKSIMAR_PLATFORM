from __future__ import annotations

from dataclasses import dataclass


def _ensure_non_empty(value: str, field_name: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f"{field_name} must be a non-empty string")
    return value.strip()


@dataclass(frozen=True)
class IOSChatNotificationBridgeContract:
    """iOS notification bridge contract.

    Contract only. It does not call iOS notification APIs.
    """

    notification_id: str
    message_id: str
    room_id: str
    title_preview: str
    sensitive_payload_allowed: bool
    direct_open_message_allowed: bool
    external_network_access_allowed: bool
    runtime_execution_allowed: bool

    def __post_init__(self) -> None:
        object.__setattr__(self, "notification_id", _ensure_non_empty(self.notification_id, "notification_id"))
        object.__setattr__(self, "message_id", _ensure_non_empty(self.message_id, "message_id"))
        object.__setattr__(self, "room_id", _ensure_non_empty(self.room_id, "room_id"))
        object.__setattr__(self, "title_preview", _ensure_non_empty(self.title_preview, "title_preview"))

        if self.sensitive_payload_allowed:
            raise ValueError("sensitive_payload_allowed must be False")
        if self.direct_open_message_allowed:
            raise ValueError("direct_open_message_allowed must be False")
        if self.external_network_access_allowed:
            raise ValueError("external_network_access_allowed must be False")
        if self.runtime_execution_allowed:
            raise ValueError("runtime_execution_allowed must be False")

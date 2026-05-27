from __future__ import annotations

from dataclasses import dataclass
from typing import Tuple


_ALLOWED_ATTACHMENT_STATES = ("declared", "scan_required", "quarantined_reference", "blocked")
_ALLOWED_STORAGE_SCOPES = ("android_private_reference", "quarantine_reference", "server_reference")


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
class AndroidFileAttachmentBridgeContract:
    """Android file attachment bridge.

    Contract only. It does not read files, write files, open Android file
    pickers, upload/download data, or call Android storage APIs.
    """

    bridge_id: str
    attachment_id: str
    message_id: str
    filename: str
    storage_scope: str
    attachment_state: str
    size_bytes: int
    checksum_required: bool
    encryption_required: bool
    scan_required: bool
    direct_file_read_allowed: bool
    direct_file_write_allowed: bool
    external_network_access_allowed: bool
    android_storage_api_call_allowed: bool

    def __post_init__(self) -> None:
        object.__setattr__(self, "bridge_id", _ensure_non_empty(self.bridge_id, "bridge_id"))
        object.__setattr__(self, "attachment_id", _ensure_non_empty(self.attachment_id, "attachment_id"))
        object.__setattr__(self, "message_id", _ensure_non_empty(self.message_id, "message_id"))
        object.__setattr__(self, "filename", _ensure_non_empty(self.filename, "filename"))
        object.__setattr__(
            self,
            "storage_scope",
            _ensure_allowed(self.storage_scope, "storage_scope", _ALLOWED_STORAGE_SCOPES),
        )
        object.__setattr__(
            self,
            "attachment_state",
            _ensure_allowed(self.attachment_state, "attachment_state", _ALLOWED_ATTACHMENT_STATES),
        )
        object.__setattr__(self, "size_bytes", _ensure_non_negative_int(self.size_bytes, "size_bytes"))

        if not self.checksum_required:
            raise ValueError("checksum_required must be True")
        if not self.encryption_required:
            raise ValueError("encryption_required must be True")
        if not self.scan_required:
            raise ValueError("scan_required must be True")
        if self.direct_file_read_allowed:
            raise ValueError("direct_file_read_allowed must be False")
        if self.direct_file_write_allowed:
            raise ValueError("direct_file_write_allowed must be False")
        if self.external_network_access_allowed:
            raise ValueError("external_network_access_allowed must be False")
        if self.android_storage_api_call_allowed:
            raise ValueError("android_storage_api_call_allowed must be False")

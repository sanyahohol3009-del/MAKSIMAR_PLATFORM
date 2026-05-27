from __future__ import annotations

from dataclasses import dataclass
from typing import Tuple


_ALLOWED_STORAGE_SCOPES = ("local_cache", "server_storage", "mobile_private_storage", "quarantine")
_ALLOWED_TRANSFER_STATES = ("declared", "queued", "blocked", "completed_reference")


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
class FileTransferContract:
    """Canonical file-transfer contract for chat attachments.

    Contract only. It does not copy files, open network connections, write to
    storage, or execute server/mobile transfer APIs.
    """

    transfer_id: str
    message_id: str
    attachment_id: str
    source_path_ref: str
    storage_scope: str
    transfer_state: str
    size_bytes: int
    checksum_required: bool
    encryption_required: bool
    direct_file_system_write_allowed: bool
    external_network_access_allowed: bool
    runtime_mutation_allowed: bool

    def __post_init__(self) -> None:
        object.__setattr__(self, "transfer_id", _ensure_non_empty(self.transfer_id, "transfer_id"))
        object.__setattr__(self, "message_id", _ensure_non_empty(self.message_id, "message_id"))
        object.__setattr__(self, "attachment_id", _ensure_non_empty(self.attachment_id, "attachment_id"))
        object.__setattr__(self, "source_path_ref", _ensure_non_empty(self.source_path_ref, "source_path_ref"))
        object.__setattr__(self, "storage_scope", _ensure_allowed(self.storage_scope, "storage_scope", _ALLOWED_STORAGE_SCOPES))
        object.__setattr__(self, "transfer_state", _ensure_allowed(self.transfer_state, "transfer_state", _ALLOWED_TRANSFER_STATES))
        object.__setattr__(self, "size_bytes", _ensure_non_negative_int(self.size_bytes, "size_bytes"))

        if not self.checksum_required:
            raise ValueError("checksum_required must be True")
        if not self.encryption_required:
            raise ValueError("encryption_required must be True")
        if self.direct_file_system_write_allowed:
            raise ValueError("direct_file_system_write_allowed must be False")
        if self.external_network_access_allowed:
            raise ValueError("external_network_access_allowed must be False")
        if self.runtime_mutation_allowed:
            raise ValueError("runtime_mutation_allowed must be False")

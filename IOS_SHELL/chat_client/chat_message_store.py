from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict, Tuple


_ALLOWED_MESSAGE_STATES = ("draft", "queued_local", "synced_reference", "blocked")


def _ensure_non_empty(value: str, field_name: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f"{field_name} must be a non-empty string")
    return value.strip()


@dataclass(frozen=True)
class IOSChatMessageStoreEntry:
    local_message_id: str
    room_id: str
    sender_identity_id: str
    text_preview: str
    message_state: str
    encrypted_at_rest: bool
    plaintext_persistence_allowed: bool
    canonical_truth_write_allowed: bool
    external_network_access_allowed: bool

    def __post_init__(self) -> None:
        object.__setattr__(self, "local_message_id", _ensure_non_empty(self.local_message_id, "local_message_id"))
        object.__setattr__(self, "room_id", _ensure_non_empty(self.room_id, "room_id"))
        object.__setattr__(self, "sender_identity_id", _ensure_non_empty(self.sender_identity_id, "sender_identity_id"))
        object.__setattr__(self, "text_preview", _ensure_non_empty(self.text_preview, "text_preview"))

        if self.message_state not in _ALLOWED_MESSAGE_STATES:
            raise ValueError(f"message_state must be one of {_ALLOWED_MESSAGE_STATES}: {self.message_state}")
        if not self.encrypted_at_rest:
            raise ValueError("encrypted_at_rest must be True")
        if self.plaintext_persistence_allowed:
            raise ValueError("plaintext_persistence_allowed must be False")
        if self.canonical_truth_write_allowed:
            raise ValueError("canonical_truth_write_allowed must be False")
        if self.external_network_access_allowed:
            raise ValueError("external_network_access_allowed must be False")


@dataclass
class IOSChatMessageStore:
    """Local in-memory iOS message store contract.

    It stores references/previews only. It does not persist plaintext, write
    canonical truth, or send data over the network.
    """

    _entries: Dict[str, IOSChatMessageStoreEntry] = field(default_factory=dict)

    def add_entry(self, entry: IOSChatMessageStoreEntry) -> IOSChatMessageStoreEntry:
        if entry.local_message_id in self._entries:
            raise ValueError(f"message already stored: {entry.local_message_id}")
        self._entries[entry.local_message_id] = entry
        return entry

    def get_entry(self, local_message_id: str) -> IOSChatMessageStoreEntry:
        local_message_id = _ensure_non_empty(local_message_id, "local_message_id")
        try:
            return self._entries[local_message_id]
        except KeyError as exc:
            raise KeyError(f"unknown local message: {local_message_id}") from exc

    def list_entries(self) -> Tuple[IOSChatMessageStoreEntry, ...]:
        return tuple(self._entries.values())

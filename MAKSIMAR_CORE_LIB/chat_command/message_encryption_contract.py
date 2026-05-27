from __future__ import annotations

from dataclasses import dataclass
from typing import Tuple


_ALLOWED_ENCRYPTION_MODES = ("at_rest_required", "in_transit_required", "end_to_end_required")
_ALLOWED_KEY_SCOPES = ("owner_device", "server_tenant", "adapter_reference")


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
class MessageEncryptionContract:
    """Canonical message encryption contract.

    Contract only. It does not generate keys, encrypt payloads, decrypt payloads,
    call external KMS, or write plaintext.
    """

    encryption_id: str
    message_id: str
    encryption_mode: str
    key_scope: str
    rotation_required: bool
    plaintext_storage_allowed: bool
    external_key_provider_allowed: bool
    runtime_mutation_allowed: bool

    def __post_init__(self) -> None:
        object.__setattr__(self, "encryption_id", _ensure_non_empty(self.encryption_id, "encryption_id"))
        object.__setattr__(self, "message_id", _ensure_non_empty(self.message_id, "message_id"))
        object.__setattr__(
            self,
            "encryption_mode",
            _ensure_allowed(self.encryption_mode, "encryption_mode", _ALLOWED_ENCRYPTION_MODES),
        )
        object.__setattr__(self, "key_scope", _ensure_allowed(self.key_scope, "key_scope", _ALLOWED_KEY_SCOPES))

        if not self.rotation_required:
            raise ValueError("rotation_required must be True")
        if self.plaintext_storage_allowed:
            raise ValueError("plaintext_storage_allowed must be False")
        if self.external_key_provider_allowed:
            raise ValueError("external_key_provider_allowed must be False")
        if self.runtime_mutation_allowed:
            raise ValueError("runtime_mutation_allowed must be False")

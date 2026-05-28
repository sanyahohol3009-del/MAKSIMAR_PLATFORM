from __future__ import annotations

from dataclasses import dataclass


_KEY_REF_PREFIXES = ("key-ref://", "keystore://", "secure-key-ref://")
_KEY_MATERIAL_MARKERS = ("-----BEGIN", "private_key", "secret=", "raw:", "base64:", "{", "[")


def _ensure_non_empty(value: str, field_name: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f"{field_name} must be a non-empty string")
    return value.strip()


def _ensure_key_ref(value: str) -> str:
    value = _ensure_non_empty(value, "key_ref")
    lowered = value.lower()
    if any(marker.lower() in lowered for marker in _KEY_MATERIAL_MARKERS):
        raise ValueError("key_ref must be a reference, not embedded key material")
    if not value.startswith(_KEY_REF_PREFIXES):
        raise ValueError(f"key_ref must start with one of {_KEY_REF_PREFIXES}")
    return value


@dataclass(frozen=True)
class AppMemoryEncryptionContract:
    """Encryption requirement contract for local mobile app memory."""

    encryption_policy_id: str
    encryption_required: bool
    at_rest_required: bool
    in_transit_requires_sync_policy: bool
    key_ref: str
    key_material_embedded: bool
    shell_keystore_required: bool
    plaintext_allowed: bool

    def __post_init__(self) -> None:
        object.__setattr__(
            self,
            "encryption_policy_id",
            _ensure_non_empty(self.encryption_policy_id, "encryption_policy_id"),
        )
        object.__setattr__(self, "key_ref", _ensure_key_ref(self.key_ref))

        required_true = {
            "encryption_required": self.encryption_required,
            "at_rest_required": self.at_rest_required,
            "in_transit_requires_sync_policy": self.in_transit_requires_sync_policy,
            "shell_keystore_required": self.shell_keystore_required,
        }
        for field_name, value in required_true.items():
            if value is not True:
                raise ValueError(f"{field_name} must be True")

        required_false = {
            "key_material_embedded": self.key_material_embedded,
            "plaintext_allowed": self.plaintext_allowed,
        }
        for field_name, value in required_false.items():
            if value is not False:
                raise ValueError(f"{field_name} must be False")

    @classmethod
    def default_mobile_encryption(
        cls,
        *,
        encryption_policy_id: str = "app_memory_encryption_default",
        key_ref: str = "keystore://app-memory/default",
    ) -> "AppMemoryEncryptionContract":
        return cls(
            encryption_policy_id=encryption_policy_id,
            encryption_required=True,
            at_rest_required=True,
            in_transit_requires_sync_policy=True,
            key_ref=key_ref,
            key_material_embedded=False,
            shell_keystore_required=True,
            plaintext_allowed=False,
        )

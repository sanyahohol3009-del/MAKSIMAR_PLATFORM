from __future__ import annotations

from dataclasses import dataclass

from shared_mobile_core.app_memory import AppMemoryEncryptionContract


_KEYCHAIN_PREFIXES = ("ios-keychain://", "keychain://", "secure-key-ref://")


def _ensure_non_empty(value: str, field_name: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f"{field_name} must be a non-empty string")
    return value.strip()


def _ensure_keychain_ref(value: str) -> str:
    value = _ensure_non_empty(value, "ios_keychain_ref")
    if not value.startswith(_KEYCHAIN_PREFIXES):
        raise ValueError("ios_keychain_ref must be a keychain reference")
    return value


@dataclass(frozen=True)
class IOSMemoryEncryptionBridge:
    bridge_id: str
    device_id: str
    app_id: str
    ios_bundle_id: str
    encryption_contract: AppMemoryEncryptionContract
    ios_keychain_ref: str
    encryption_required: bool
    at_rest_required: bool
    in_transit_requires_sync_policy: bool
    key_material_embedded: bool
    plaintext_allowed: bool
    shell_adapter_only: bool
    canonical_truth: bool
    core_write_allowed: bool
    direct_server_write_allowed: bool
    platform_api_calls_allowed: bool

    def __post_init__(self) -> None:
        for field_name in ("bridge_id", "device_id", "app_id", "ios_bundle_id"):
            object.__setattr__(self, field_name, _ensure_non_empty(getattr(self, field_name), field_name))

        if not isinstance(self.encryption_contract, AppMemoryEncryptionContract):
            raise ValueError("encryption_contract must be AppMemoryEncryptionContract")
        object.__setattr__(self, "ios_keychain_ref", _ensure_keychain_ref(self.ios_keychain_ref))

        required_true = {
            "encryption_required": self.encryption_required,
            "at_rest_required": self.at_rest_required,
            "in_transit_requires_sync_policy": self.in_transit_requires_sync_policy,
            "shell_adapter_only": self.shell_adapter_only,
        }
        for field_name, value in required_true.items():
            if value is not True:
                raise ValueError(f"{field_name} must be True")

        required_false = {
            "key_material_embedded": self.key_material_embedded,
            "plaintext_allowed": self.plaintext_allowed,
            "canonical_truth": self.canonical_truth,
            "core_write_allowed": self.core_write_allowed,
            "direct_server_write_allowed": self.direct_server_write_allowed,
            "platform_api_calls_allowed": self.platform_api_calls_allowed,
        }
        for field_name, value in required_false.items():
            if value is not False:
                raise ValueError(f"{field_name} must be False")

        if self.encryption_contract.key_material_embedded:
            raise ValueError("encryption_contract key material must not be embedded")
        if self.encryption_contract.plaintext_allowed:
            raise ValueError("encryption_contract plaintext must not be allowed")

    @classmethod
    def default_bridge(
        cls,
        *,
        bridge_id: str,
        device_id: str,
        app_id: str,
        ios_bundle_id: str,
    ) -> "IOSMemoryEncryptionBridge":
        encryption_contract = AppMemoryEncryptionContract.default_mobile_encryption(
            encryption_policy_id=f"{bridge_id}_policy",
            key_ref=f"secure-key-ref://{device_id}/app-memory/default",
        )
        return cls(
            bridge_id=bridge_id,
            device_id=device_id,
            app_id=app_id,
            ios_bundle_id=ios_bundle_id,
            encryption_contract=encryption_contract,
            ios_keychain_ref=f"ios-keychain://{device_id}/app-memory/default",
            encryption_required=True,
            at_rest_required=True,
            in_transit_requires_sync_policy=True,
            key_material_embedded=False,
            plaintext_allowed=False,
            shell_adapter_only=True,
            canonical_truth=False,
            core_write_allowed=False,
            direct_server_write_allowed=False,
            platform_api_calls_allowed=False,
        )

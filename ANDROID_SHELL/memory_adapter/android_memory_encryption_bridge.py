from __future__ import annotations

from dataclasses import dataclass

from shared_mobile_core.app_memory import AppMemoryEncryptionContract


_KEYSTORE_PREFIXES = ("android-keystore://", "keystore://", "secure-key-ref://")


def _ensure_non_empty(value: str, field_name: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f"{field_name} must be a non-empty string")
    return value.strip()


def _ensure_keystore_ref(value: str) -> str:
    value = _ensure_non_empty(value, "android_keystore_ref")
    if not value.startswith(_KEYSTORE_PREFIXES):
        raise ValueError("android_keystore_ref must be a keystore reference")
    return value


@dataclass(frozen=True)
class AndroidMemoryEncryptionBridge:
    bridge_id: str
    device_id: str
    app_id: str
    android_package_name: str
    encryption_contract: AppMemoryEncryptionContract
    android_keystore_ref: str
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
        for field_name in ("bridge_id", "device_id", "app_id", "android_package_name"):
            object.__setattr__(self, field_name, _ensure_non_empty(getattr(self, field_name), field_name))

        if not isinstance(self.encryption_contract, AppMemoryEncryptionContract):
            raise ValueError("encryption_contract must be AppMemoryEncryptionContract")
        object.__setattr__(self, "android_keystore_ref", _ensure_keystore_ref(self.android_keystore_ref))

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
        android_package_name: str,
    ) -> "AndroidMemoryEncryptionBridge":
        encryption_contract = AppMemoryEncryptionContract.default_mobile_encryption(
            encryption_policy_id=f"{bridge_id}_policy",
            key_ref=f"keystore://{device_id}/app-memory/default",
        )
        return cls(
            bridge_id=bridge_id,
            device_id=device_id,
            app_id=app_id,
            android_package_name=android_package_name,
            encryption_contract=encryption_contract,
            android_keystore_ref=f"android-keystore://{device_id}/app-memory/default",
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

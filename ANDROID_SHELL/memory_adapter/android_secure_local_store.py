from __future__ import annotations

from dataclasses import dataclass


_ALLOWED_STORAGE_SCOPES = ("android_app_sandbox", "android_keystore_reference", "android_private_storage")
_REF_PREFIXES = ("android-secure-ref://", "secure-ref://")


def _ensure_non_empty(value: str, field_name: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f"{field_name} must be a non-empty string")
    return value.strip()


def _ensure_ref(value: str, field_name: str) -> str:
    value = _ensure_non_empty(value, field_name)
    if not value.startswith(_REF_PREFIXES):
        raise ValueError(f"{field_name} must be a secure reference")
    return value


@dataclass(frozen=True)
class AndroidSecureLocalStore:
    local_store_id: str
    device_id: str
    app_id: str
    android_package_name: str
    storage_scope: str
    storage_ref: str
    encrypted_at_rest_required: bool
    key_material_embedded: bool
    plaintext_allowed: bool
    local_app_memory_only: bool
    shell_adapter_only: bool
    canonical_truth: bool
    core_write_allowed: bool
    direct_server_write_allowed: bool
    file_io_allowed: bool
    network_allowed: bool
    supported_record_kinds: tuple[str, ...]

    def __post_init__(self) -> None:
        for field_name in ("local_store_id", "device_id", "app_id", "android_package_name"):
            object.__setattr__(self, field_name, _ensure_non_empty(getattr(self, field_name), field_name))

        object.__setattr__(self, "storage_scope", _ensure_non_empty(self.storage_scope, "storage_scope"))
        if self.storage_scope not in _ALLOWED_STORAGE_SCOPES:
            raise ValueError(f"storage_scope must be one of {_ALLOWED_STORAGE_SCOPES}")

        object.__setattr__(self, "storage_ref", _ensure_ref(self.storage_ref, "storage_ref"))

        if not isinstance(self.supported_record_kinds, tuple) or not self.supported_record_kinds:
            raise ValueError("supported_record_kinds must be a non-empty tuple")
        normalized = tuple(_ensure_non_empty(value, "supported_record_kind") for value in self.supported_record_kinds)
        if len(set(normalized)) != len(normalized):
            raise ValueError("supported_record_kinds must not contain duplicates")
        object.__setattr__(self, "supported_record_kinds", normalized)

        required_true = {
            "encrypted_at_rest_required": self.encrypted_at_rest_required,
            "local_app_memory_only": self.local_app_memory_only,
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
            "file_io_allowed": self.file_io_allowed,
            "network_allowed": self.network_allowed,
        }
        for field_name, value in required_false.items():
            if value is not False:
                raise ValueError(f"{field_name} must be False")

    @classmethod
    def default_secure_store(
        cls,
        *,
        local_store_id: str,
        device_id: str,
        app_id: str,
        android_package_name: str,
    ) -> "AndroidSecureLocalStore":
        return cls(
            local_store_id=local_store_id,
            device_id=device_id,
            app_id=app_id,
            android_package_name=android_package_name,
            storage_scope="android_app_sandbox",
            storage_ref=f"android-secure-ref://{device_id}/app-memory/{local_store_id}",
            encrypted_at_rest_required=True,
            key_material_embedded=False,
            plaintext_allowed=False,
            local_app_memory_only=True,
            shell_adapter_only=True,
            canonical_truth=False,
            core_write_allowed=False,
            direct_server_write_allowed=False,
            file_io_allowed=False,
            network_allowed=False,
            supported_record_kinds=("app_state", "preference", "ui_state_ref", "device_setting"),
        )

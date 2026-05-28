from __future__ import annotations

from dataclasses import dataclass
from typing import Tuple


_ALLOWED_STORAGE_SCOPES = ("device_private", "app_sandbox", "secure_local_reference")
_DEFAULT_RECORD_KINDS = ("app_state", "preference", "ui_state_ref", "device_setting")


def _ensure_non_empty(value: str, field_name: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f"{field_name} must be a non-empty string")
    return value.strip()


def _ensure_supported_record_kinds(values: Tuple[str, ...]) -> Tuple[str, ...]:
    if not isinstance(values, tuple) or not values:
        raise ValueError("supported_record_kinds must be a non-empty tuple")
    normalized = tuple(_ensure_non_empty(value, "supported_record_kind") for value in values)
    if len(set(normalized)) != len(normalized):
        raise ValueError("supported_record_kinds must not contain duplicates")
    return normalized


@dataclass(frozen=True)
class AppMemoryStoreContract:
    """Local mobile app memory store contract.

    The store is an adapter boundary. It does not perform persistence, write
    MAKSIMAR core, or define server canonical truth.
    """

    store_id: str
    device_id: str
    app_id: str
    owner_identity_id: str
    storage_scope: str
    encrypted_at_rest_required: bool
    retention_required: bool
    offline_first: bool
    sync_policy_required: bool
    shell_adapter_only: bool
    canonical_truth: bool
    core_write_allowed: bool
    direct_server_write_allowed: bool
    supported_record_kinds: Tuple[str, ...]

    def __post_init__(self) -> None:
        for field_name in ("store_id", "device_id", "app_id", "owner_identity_id"):
            object.__setattr__(self, field_name, _ensure_non_empty(getattr(self, field_name), field_name))

        object.__setattr__(self, "storage_scope", _ensure_non_empty(self.storage_scope, "storage_scope"))
        if self.storage_scope not in _ALLOWED_STORAGE_SCOPES:
            raise ValueError(f"storage_scope must be one of {_ALLOWED_STORAGE_SCOPES}: {self.storage_scope}")
        object.__setattr__(
            self,
            "supported_record_kinds",
            _ensure_supported_record_kinds(self.supported_record_kinds),
        )

        required_true = {
            "encrypted_at_rest_required": self.encrypted_at_rest_required,
            "retention_required": self.retention_required,
            "offline_first": self.offline_first,
            "sync_policy_required": self.sync_policy_required,
            "shell_adapter_only": self.shell_adapter_only,
        }
        for field_name, value in required_true.items():
            if value is not True:
                raise ValueError(f"{field_name} must be True")

        required_false = {
            "canonical_truth": self.canonical_truth,
            "core_write_allowed": self.core_write_allowed,
            "direct_server_write_allowed": self.direct_server_write_allowed,
        }
        for field_name, value in required_false.items():
            if value is not False:
                raise ValueError(f"{field_name} must be False")

    @classmethod
    def default_mobile_store(
        cls,
        *,
        store_id: str,
        device_id: str,
        app_id: str,
        owner_identity_id: str,
    ) -> "AppMemoryStoreContract":
        return cls(
            store_id=store_id,
            device_id=device_id,
            app_id=app_id,
            owner_identity_id=owner_identity_id,
            storage_scope="app_sandbox",
            encrypted_at_rest_required=True,
            retention_required=True,
            offline_first=True,
            sync_policy_required=True,
            shell_adapter_only=True,
            canonical_truth=False,
            core_write_allowed=False,
            direct_server_write_allowed=False,
            supported_record_kinds=_DEFAULT_RECORD_KINDS,
        )

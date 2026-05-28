from __future__ import annotations

from dataclasses import dataclass
from typing import Tuple


_ALLOWED_MEMORY_SCOPES = ("local_app_state", "user_preferences", "ui_session_state", "device_local_settings")
_ALLOWED_MEMORY_KINDS = ("app_state", "preference", "ui_state_ref", "device_setting")
_ALLOWED_PRIVACY_CLASSES = ("local_private", "owner_private", "device_private")
_REFERENCE_PREFIXES = ("ref://", "local://", "app-memory://", "secure-ref://")
_INLINE_PAYLOAD_MARKERS = ("{", "[", "base64:", "data:", "inline:", "payload:")


def _ensure_non_empty(value: str, field_name: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f"{field_name} must be a non-empty string")
    return value.strip()


def _ensure_allowed(value: str, field_name: str, allowed: Tuple[str, ...]) -> str:
    value = _ensure_non_empty(value, field_name)
    if value not in allowed:
        raise ValueError(f"{field_name} must be one of {allowed}: {value}")
    return value


def _ensure_payload_ref(value: str) -> str:
    value = _ensure_non_empty(value, "payload_ref")
    lowered = value.lower()
    if any(marker in lowered for marker in _INLINE_PAYLOAD_MARKERS):
        raise ValueError("payload_ref must be a reference, not inline payload")
    if not value.startswith(_REFERENCE_PREFIXES):
        raise ValueError(f"payload_ref must start with one of {_REFERENCE_PREFIXES}")
    return value


@dataclass(frozen=True)
class AppMemoryRecordContract:
    """Local mobile app memory record contract.

    This contract models device-local app state only. It does not persist data,
    write core memory, call a server, or define canonical project truth.
    """

    record_id: str
    app_id: str
    device_id: str
    owner_identity_id: str
    memory_scope: str
    memory_kind: str
    payload_ref: str
    created_at: str
    updated_at: str
    schema_version: str
    privacy_classification: str
    retention_policy_id: str
    encryption_policy_id: str
    sync_eligible: bool
    sync_requires_policy: bool
    audit_ref: str
    local_app_memory_only: bool
    global_project_memory: bool
    canonical_truth: bool
    core_write_allowed: bool
    direct_server_write_allowed: bool

    def __post_init__(self) -> None:
        for field_name in (
            "record_id",
            "app_id",
            "device_id",
            "owner_identity_id",
            "created_at",
            "updated_at",
            "schema_version",
            "retention_policy_id",
            "encryption_policy_id",
            "audit_ref",
        ):
            object.__setattr__(self, field_name, _ensure_non_empty(getattr(self, field_name), field_name))

        object.__setattr__(
            self,
            "memory_scope",
            _ensure_allowed(self.memory_scope, "memory_scope", _ALLOWED_MEMORY_SCOPES),
        )
        object.__setattr__(
            self,
            "memory_kind",
            _ensure_allowed(self.memory_kind, "memory_kind", _ALLOWED_MEMORY_KINDS),
        )
        object.__setattr__(
            self,
            "privacy_classification",
            _ensure_allowed(self.privacy_classification, "privacy_classification", _ALLOWED_PRIVACY_CLASSES),
        )
        object.__setattr__(self, "payload_ref", _ensure_payload_ref(self.payload_ref))

        if not self.sync_requires_policy:
            raise ValueError("sync_requires_policy must be True")
        if not self.local_app_memory_only:
            raise ValueError("local_app_memory_only must be True")
        if self.global_project_memory:
            raise ValueError("global_project_memory must be False")
        if self.canonical_truth:
            raise ValueError("canonical_truth must be False")
        if self.core_write_allowed:
            raise ValueError("core_write_allowed must be False")
        if self.direct_server_write_allowed:
            raise ValueError("direct_server_write_allowed must be False")

    @classmethod
    def local_preference(
        cls,
        *,
        record_id: str,
        app_id: str,
        device_id: str,
        owner_identity_id: str,
        payload_ref: str,
        created_at: str,
        updated_at: str,
        retention_policy_id: str,
        encryption_policy_id: str,
        audit_ref: str,
        sync_eligible: bool = True,
    ) -> "AppMemoryRecordContract":
        return cls(
            record_id=record_id,
            app_id=app_id,
            device_id=device_id,
            owner_identity_id=owner_identity_id,
            memory_scope="user_preferences",
            memory_kind="preference",
            payload_ref=payload_ref,
            created_at=created_at,
            updated_at=updated_at,
            schema_version="app_memory_record.v1",
            privacy_classification="owner_private",
            retention_policy_id=retention_policy_id,
            encryption_policy_id=encryption_policy_id,
            sync_eligible=sync_eligible,
            sync_requires_policy=True,
            audit_ref=audit_ref,
            local_app_memory_only=True,
            global_project_memory=False,
            canonical_truth=False,
            core_write_allowed=False,
            direct_server_write_allowed=False,
        )

    @classmethod
    def local_app_state(
        cls,
        *,
        record_id: str,
        app_id: str,
        device_id: str,
        owner_identity_id: str,
        payload_ref: str,
        created_at: str,
        updated_at: str,
        retention_policy_id: str,
        encryption_policy_id: str,
        audit_ref: str,
    ) -> "AppMemoryRecordContract":
        return cls(
            record_id=record_id,
            app_id=app_id,
            device_id=device_id,
            owner_identity_id=owner_identity_id,
            memory_scope="local_app_state",
            memory_kind="app_state",
            payload_ref=payload_ref,
            created_at=created_at,
            updated_at=updated_at,
            schema_version="app_memory_record.v1",
            privacy_classification="local_private",
            retention_policy_id=retention_policy_id,
            encryption_policy_id=encryption_policy_id,
            sync_eligible=True,
            sync_requires_policy=True,
            audit_ref=audit_ref,
            local_app_memory_only=True,
            global_project_memory=False,
            canonical_truth=False,
            core_write_allowed=False,
            direct_server_write_allowed=False,
        )

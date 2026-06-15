from __future__ import annotations

from dataclasses import dataclass
from typing import Any


def _ensure_non_empty(value: str, field_name: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f"{field_name} must be a non-empty string")
    return value.strip()


def _require_true(value: bool, field_name: str) -> None:
    if value is not True:
        raise ValueError(f"{field_name} must be True")


def _require_false(value: bool, field_name: str) -> None:
    if value is not False:
        raise ValueError(f"{field_name} must be False")


@dataclass(frozen=True)
class AppSafeCoreExportManifest:
    manifest_id: str
    exportable_slices: tuple[str, ...]
    raw_canonical_core_export_allowed: bool
    secret_export_allowed: bool
    approval_security_core_export_allowed: bool
    owner_identity_secret_export_allowed: bool
    raw_memory_dump_allowed: bool
    private_file_dump_allowed: bool
    runtime_token_export_allowed: bool
    export_is_read_only: bool
    export_is_intent_only: bool
    export_requires_policy: bool
    mobile_cache_allowed: bool
    mobile_cache_canonical: bool

    def __post_init__(self) -> None:
        object.__setattr__(self, "manifest_id", _ensure_non_empty(self.manifest_id, "manifest_id"))
        if not isinstance(self.exportable_slices, tuple) or not self.exportable_slices:
            raise ValueError("exportable_slices must be a non-empty tuple")
        normalized = tuple(_ensure_non_empty(value, "exportable_slice") for value in self.exportable_slices)
        if len(set(normalized)) != len(normalized):
            raise ValueError("exportable_slices must not contain duplicates")
        object.__setattr__(self, "exportable_slices", normalized)

        _require_false(
            self.raw_canonical_core_export_allowed,
            "raw_canonical_core_export_allowed",
        )
        _require_false(self.secret_export_allowed, "secret_export_allowed")
        _require_false(
            self.approval_security_core_export_allowed,
            "approval_security_core_export_allowed",
        )
        _require_false(
            self.owner_identity_secret_export_allowed,
            "owner_identity_secret_export_allowed",
        )
        _require_false(self.raw_memory_dump_allowed, "raw_memory_dump_allowed")
        _require_false(self.private_file_dump_allowed, "private_file_dump_allowed")
        _require_false(self.runtime_token_export_allowed, "runtime_token_export_allowed")
        _require_true(self.export_is_read_only, "export_is_read_only")
        _require_true(self.export_is_intent_only, "export_is_intent_only")
        _require_true(self.export_requires_policy, "export_requires_policy")
        _require_true(self.mobile_cache_allowed, "mobile_cache_allowed")
        _require_false(self.mobile_cache_canonical, "mobile_cache_canonical")

    def to_read_model(self) -> dict[str, Any]:
        return {
            "manifest_id": self.manifest_id,
            "exportable_slices": self.exportable_slices,
            "raw_canonical_core_export_allowed": self.raw_canonical_core_export_allowed,
            "secret_export_allowed": self.secret_export_allowed,
            "approval_security_core_export_allowed": (
                self.approval_security_core_export_allowed
            ),
            "owner_identity_secret_export_allowed": (
                self.owner_identity_secret_export_allowed
            ),
            "raw_memory_dump_allowed": self.raw_memory_dump_allowed,
            "private_file_dump_allowed": self.private_file_dump_allowed,
            "runtime_token_export_allowed": self.runtime_token_export_allowed,
            "export_is_read_only": self.export_is_read_only,
            "export_is_intent_only": self.export_is_intent_only,
            "export_requires_policy": self.export_requires_policy,
            "mobile_cache_allowed": self.mobile_cache_allowed,
            "mobile_cache_canonical": self.mobile_cache_canonical,
        }


def build_app_safe_core_export_manifest() -> AppSafeCoreExportManifest:
    return AppSafeCoreExportManifest(
        manifest_id="app_safe_core_export_manifest_v0_1",
        exportable_slices=(
            "app_safe_intent_context",
            "app_safe_read_only_summary",
            "app_safe_ui_state_reference",
        ),
        raw_canonical_core_export_allowed=False,
        secret_export_allowed=False,
        approval_security_core_export_allowed=False,
        owner_identity_secret_export_allowed=False,
        raw_memory_dump_allowed=False,
        private_file_dump_allowed=False,
        runtime_token_export_allowed=False,
        export_is_read_only=True,
        export_is_intent_only=True,
        export_requires_policy=True,
        mobile_cache_allowed=True,
        mobile_cache_canonical=False,
    )

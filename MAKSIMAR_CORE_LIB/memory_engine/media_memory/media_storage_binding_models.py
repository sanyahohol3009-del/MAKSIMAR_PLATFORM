from __future__ import annotations

import re
from dataclasses import dataclass


_MEDIA_ARTIFACT_ID_PATTERN = re.compile(r"^media_artifact_[a-z][a-z0-9_]*$")
_STORAGE_REGISTRY_ID_PATTERN = re.compile(r"^storage_registry_[a-z][a-z0-9_]*$")


def _ensure_non_empty_str(value: str, field_name: str) -> str:
    if not isinstance(value, str):
        raise ValueError(f"{field_name} must be a string")
    normalized = value.strip()
    if not normalized:
        raise ValueError(f"{field_name} must be a non-empty string")
    return normalized


def _ensure_non_negative_int(value: int, field_name: str) -> int:
    if not isinstance(value, int):
        raise ValueError(f"{field_name} must be an int")
    if value < 0:
        raise ValueError(f"{field_name} must be >= 0")
    return value


def _ensure_bool(value: bool, field_name: str) -> bool:
    if not isinstance(value, bool):
        raise ValueError(f"{field_name} must be bool")
    return value


@dataclass(frozen=True, slots=True)
class MediaStorageBindingEntry:
    """Read-only binding from media memory record to storage registry entry."""

    artifact_id: str
    artifact_ref: str
    artifact_kind: str
    storage_registry_id: str
    storage_entry_kind: str
    binary_external: bool
    dashboard_visible: bool
    retrieval_visible: bool
    storage_binding_ready: bool

    def __post_init__(self) -> None:
        artifact_id = _ensure_non_empty_str(self.artifact_id, "artifact_id")
        artifact_ref = _ensure_non_empty_str(self.artifact_ref, "artifact_ref")
        artifact_kind = _ensure_non_empty_str(self.artifact_kind, "artifact_kind")
        storage_registry_id = _ensure_non_empty_str(
            self.storage_registry_id,
            "storage_registry_id",
        )
        storage_entry_kind = _ensure_non_empty_str(
            self.storage_entry_kind,
            "storage_entry_kind",
        )

        if not _MEDIA_ARTIFACT_ID_PATTERN.fullmatch(artifact_id):
            raise ValueError(f"Invalid artifact_id: {artifact_id}")
        if not _STORAGE_REGISTRY_ID_PATTERN.fullmatch(storage_registry_id):
            raise ValueError(f"Invalid storage_registry_id: {storage_registry_id}")

        for field_name in (
            "binary_external",
            "dashboard_visible",
            "retrieval_visible",
            "storage_binding_ready",
        ):
            _ensure_bool(getattr(self, field_name), field_name)

        if not self.binary_external:
            raise ValueError("media storage binding requires binary_external=True")
        if not self.storage_binding_ready:
            raise ValueError("storage_binding_ready must be True")

        object.__setattr__(self, "artifact_id", artifact_id)
        object.__setattr__(self, "artifact_ref", artifact_ref)
        object.__setattr__(self, "artifact_kind", artifact_kind)
        object.__setattr__(self, "storage_registry_id", storage_registry_id)
        object.__setattr__(self, "storage_entry_kind", storage_entry_kind)


@dataclass(frozen=True, slots=True)
class MediaStorageBindingContract:
    """Read-only contract for media memory to storage registry binding."""

    total_bindings: int
    storage_ready_bindings: int
    dashboard_visible_bindings: int
    retrieval_visible_bindings: int
    binary_external_bindings: int
    binding_ready: bool
    entries: tuple[MediaStorageBindingEntry, ...]

    def __post_init__(self) -> None:
        total_bindings = _ensure_non_negative_int(
            self.total_bindings,
            "total_bindings",
        )
        storage_ready_bindings = _ensure_non_negative_int(
            self.storage_ready_bindings,
            "storage_ready_bindings",
        )
        dashboard_visible_bindings = _ensure_non_negative_int(
            self.dashboard_visible_bindings,
            "dashboard_visible_bindings",
        )
        retrieval_visible_bindings = _ensure_non_negative_int(
            self.retrieval_visible_bindings,
            "retrieval_visible_bindings",
        )
        binary_external_bindings = _ensure_non_negative_int(
            self.binary_external_bindings,
            "binary_external_bindings",
        )

        if total_bindings != len(self.entries):
            raise ValueError("total_bindings must match entries length")

        if storage_ready_bindings != sum(
            1 for entry in self.entries if entry.storage_binding_ready
        ):
            raise ValueError("storage_ready_bindings must match computed count")

        if dashboard_visible_bindings != sum(
            1 for entry in self.entries if entry.dashboard_visible
        ):
            raise ValueError("dashboard_visible_bindings must match computed count")

        if retrieval_visible_bindings != sum(
            1 for entry in self.entries if entry.retrieval_visible
        ):
            raise ValueError("retrieval_visible_bindings must match computed count")

        if binary_external_bindings != sum(
            1 for entry in self.entries if entry.binary_external
        ):
            raise ValueError("binary_external_bindings must match computed count")

        if not isinstance(self.binding_ready, bool):
            raise ValueError("binding_ready must be bool")

        computed_ready = (
            total_bindings >= 1
            and storage_ready_bindings == total_bindings
            and binary_external_bindings == total_bindings
        )
        if self.binding_ready != computed_ready:
            raise ValueError("binding_ready must match computed readiness")

        artifact_ids = tuple(entry.artifact_id for entry in self.entries)
        if len(set(artifact_ids)) != len(artifact_ids):
            raise ValueError("duplicate artifact_id values detected")

        object.__setattr__(self, "total_bindings", total_bindings)
        object.__setattr__(self, "storage_ready_bindings", storage_ready_bindings)
        object.__setattr__(self, "dashboard_visible_bindings", dashboard_visible_bindings)
        object.__setattr__(self, "retrieval_visible_bindings", retrieval_visible_bindings)
        object.__setattr__(self, "binary_external_bindings", binary_external_bindings)

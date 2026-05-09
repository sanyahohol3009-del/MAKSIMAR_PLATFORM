from __future__ import annotations

import re
from dataclasses import dataclass


_STORAGE_REGISTRY_ID_PATTERN = re.compile(r"^storage_registry_[a-z][a-z0-9_]*$")
_COLLECTION_ID_PATTERN = re.compile(r"^artifact_collection_[a-z][a-z0-9_]*$")


def _ensure_non_empty_str(value: str, field_name: str) -> str:
    if not isinstance(value, str):
        raise ValueError(f"{field_name} must be a string")
    normalized = value.strip()
    if not normalized:
        raise ValueError(f"{field_name} must be a non-empty string")
    return normalized


def _ensure_optional_str(value: str, field_name: str) -> str:
    if not isinstance(value, str):
        raise ValueError(f"{field_name} must be a string")
    return value.strip()


def _ensure_non_negative_int(value: int, field_name: str) -> int:
    if not isinstance(value, int):
        raise ValueError(f"{field_name} must be an int")
    if value < 0:
        raise ValueError(f"{field_name} must be >= 0")
    return value


@dataclass(frozen=True, slots=True)
class StorageArtifactRoutingBindingEntry:
    """Read-only binding between artifact routing and storage registry."""

    request_id: str
    route_target: str
    routing_status: str
    artifact_ref: str
    owner_task_id: str
    storage_registry_id: str
    artifact_collection_id: str
    storage_binding_required: bool
    storage_binding_ready: bool
    data_plane_binding_ready: bool
    dashboard_visible: bool

    def __post_init__(self) -> None:
        request_id = _ensure_non_empty_str(self.request_id, "request_id")
        route_target = _ensure_non_empty_str(self.route_target, "route_target")
        routing_status = _ensure_non_empty_str(self.routing_status, "routing_status")
        artifact_ref = _ensure_optional_str(self.artifact_ref, "artifact_ref")
        owner_task_id = _ensure_optional_str(self.owner_task_id, "owner_task_id")
        storage_registry_id = _ensure_optional_str(
            self.storage_registry_id,
            "storage_registry_id",
        )
        artifact_collection_id = _ensure_optional_str(
            self.artifact_collection_id,
            "artifact_collection_id",
        )

        for field_name in (
            "storage_binding_required",
            "storage_binding_ready",
            "data_plane_binding_ready",
            "dashboard_visible",
        ):
            if not isinstance(getattr(self, field_name), bool):
                raise ValueError(f"{field_name} must be bool")

        if self.storage_binding_required:
            if not artifact_ref:
                raise ValueError("artifact_ref is required for storage binding")
            if not owner_task_id:
                raise ValueError("owner_task_id is required for storage binding")
            if not _STORAGE_REGISTRY_ID_PATTERN.fullmatch(storage_registry_id):
                raise ValueError(f"Invalid storage_registry_id: {storage_registry_id}")
            if not _COLLECTION_ID_PATTERN.fullmatch(artifact_collection_id):
                raise ValueError(
                    f"Invalid artifact_collection_id: {artifact_collection_id}"
                )

        object.__setattr__(self, "request_id", request_id)
        object.__setattr__(self, "route_target", route_target)
        object.__setattr__(self, "routing_status", routing_status)
        object.__setattr__(self, "artifact_ref", artifact_ref)
        object.__setattr__(self, "owner_task_id", owner_task_id)
        object.__setattr__(self, "storage_registry_id", storage_registry_id)
        object.__setattr__(self, "artifact_collection_id", artifact_collection_id)


@dataclass(frozen=True, slots=True)
class StorageArtifactRoutingBindingContract:
    """Read-only contract for storage/artifact/data-plane binding."""

    total_entries: int
    storage_required_entries: int
    storage_ready_entries: int
    data_plane_ready_entries: int
    dashboard_visible_entries: int
    binding_ready: bool
    entries: tuple[StorageArtifactRoutingBindingEntry, ...]

    def __post_init__(self) -> None:
        total_entries = _ensure_non_negative_int(self.total_entries, "total_entries")
        storage_required_entries = _ensure_non_negative_int(
            self.storage_required_entries,
            "storage_required_entries",
        )
        storage_ready_entries = _ensure_non_negative_int(
            self.storage_ready_entries,
            "storage_ready_entries",
        )
        data_plane_ready_entries = _ensure_non_negative_int(
            self.data_plane_ready_entries,
            "data_plane_ready_entries",
        )
        dashboard_visible_entries = _ensure_non_negative_int(
            self.dashboard_visible_entries,
            "dashboard_visible_entries",
        )

        if total_entries != len(self.entries):
            raise ValueError("total_entries must match entries length")

        if storage_required_entries != sum(
            1 for entry in self.entries if entry.storage_binding_required
        ):
            raise ValueError("storage_required_entries must match computed count")

        if storage_ready_entries != sum(
            1
            for entry in self.entries
            if entry.storage_binding_required and entry.storage_binding_ready
        ):
            raise ValueError("storage_ready_entries must match computed count")

        if data_plane_ready_entries != sum(
            1
            for entry in self.entries
            if entry.storage_binding_required and entry.data_plane_binding_ready
        ):
            raise ValueError("data_plane_ready_entries must match computed count")

        if dashboard_visible_entries != sum(
            1 for entry in self.entries if entry.dashboard_visible
        ):
            raise ValueError("dashboard_visible_entries must match computed count")

        if not isinstance(self.binding_ready, bool):
            raise ValueError("binding_ready must be bool")

        request_ids = tuple(entry.request_id for entry in self.entries)
        if len(set(request_ids)) != len(request_ids):
            raise ValueError("Duplicate request_id values detected")

        required_entries = tuple(
            entry for entry in self.entries if entry.storage_binding_required
        )
        computed_ready = all(
            entry.storage_binding_ready and entry.data_plane_binding_ready
            for entry in required_entries
        )

        if self.binding_ready != computed_ready:
            raise ValueError("binding_ready must match required entry readiness")

        object.__setattr__(self, "total_entries", total_entries)
        object.__setattr__(self, "storage_required_entries", storage_required_entries)
        object.__setattr__(self, "storage_ready_entries", storage_ready_entries)
        object.__setattr__(self, "data_plane_ready_entries", data_plane_ready_entries)
        object.__setattr__(self, "dashboard_visible_entries", dashboard_visible_entries)

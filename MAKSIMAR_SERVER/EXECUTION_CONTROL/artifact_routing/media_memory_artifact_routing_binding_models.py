from __future__ import annotations

import re
from dataclasses import dataclass


_MEDIA_ARTIFACT_ID_PATTERN = re.compile(r"^media_artifact_[a-z][a-z0-9_]*$")


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


def _ensure_bool(value: bool, field_name: str) -> bool:
    if not isinstance(value, bool):
        raise ValueError(f"{field_name} must be bool")
    return value


@dataclass(frozen=True, slots=True)
class MediaMemoryArtifactRoutingEntry:
    """Read-only binding between media memory and artifact routing."""

    media_artifact_id: str
    media_artifact_ref: str
    storage_registry_id: str
    route_request_id: str
    route_target: str
    route_binding_required: bool
    route_binding_ready: bool
    dashboard_visible: bool

    def __post_init__(self) -> None:
        media_artifact_id = _ensure_non_empty_str(
            self.media_artifact_id,
            "media_artifact_id",
        )
        media_artifact_ref = _ensure_non_empty_str(
            self.media_artifact_ref,
            "media_artifact_ref",
        )
        storage_registry_id = _ensure_non_empty_str(
            self.storage_registry_id,
            "storage_registry_id",
        )
        route_request_id = _ensure_optional_str(
            self.route_request_id,
            "route_request_id",
        )
        route_target = _ensure_optional_str(self.route_target, "route_target")

        for field_name in (
            "route_binding_required",
            "route_binding_ready",
            "dashboard_visible",
        ):
            _ensure_bool(getattr(self, field_name), field_name)

        if not _MEDIA_ARTIFACT_ID_PATTERN.fullmatch(media_artifact_id):
            raise ValueError(f"Invalid media_artifact_id: {media_artifact_id}")

        if self.route_binding_required:
            if not route_request_id:
                raise ValueError("route_request_id is required when route binding is required")
            if not route_target:
                raise ValueError("route_target is required when route binding is required")
            if not self.route_binding_ready:
                raise ValueError("route_binding_ready must be True for required routes")

        object.__setattr__(self, "media_artifact_id", media_artifact_id)
        object.__setattr__(self, "media_artifact_ref", media_artifact_ref)
        object.__setattr__(self, "storage_registry_id", storage_registry_id)
        object.__setattr__(self, "route_request_id", route_request_id)
        object.__setattr__(self, "route_target", route_target)


@dataclass(frozen=True, slots=True)
class MediaMemoryArtifactRoutingContract:
    """Read-only media memory / artifact routing binding contract."""

    total_entries: int
    route_required_entries: int
    route_ready_entries: int
    dashboard_visible_entries: int
    binding_ready: bool
    entries: tuple[MediaMemoryArtifactRoutingEntry, ...]

    def __post_init__(self) -> None:
        total_entries = _ensure_non_negative_int(self.total_entries, "total_entries")
        route_required_entries = _ensure_non_negative_int(
            self.route_required_entries,
            "route_required_entries",
        )
        route_ready_entries = _ensure_non_negative_int(
            self.route_ready_entries,
            "route_ready_entries",
        )
        dashboard_visible_entries = _ensure_non_negative_int(
            self.dashboard_visible_entries,
            "dashboard_visible_entries",
        )

        if total_entries != len(self.entries):
            raise ValueError("total_entries must match entries length")

        if route_required_entries != sum(
            1 for entry in self.entries if entry.route_binding_required
        ):
            raise ValueError("route_required_entries must match computed count")

        if route_ready_entries != sum(
            1
            for entry in self.entries
            if entry.route_binding_required and entry.route_binding_ready
        ):
            raise ValueError("route_ready_entries must match computed count")

        if dashboard_visible_entries != sum(
            1 for entry in self.entries if entry.dashboard_visible
        ):
            raise ValueError("dashboard_visible_entries must match computed count")

        if not isinstance(self.binding_ready, bool):
            raise ValueError("binding_ready must be bool")

        computed_ready = (
            route_required_entries >= 1
            and route_ready_entries == route_required_entries
        )
        if self.binding_ready != computed_ready:
            raise ValueError("binding_ready must match computed readiness")

        object.__setattr__(self, "total_entries", total_entries)
        object.__setattr__(self, "route_required_entries", route_required_entries)
        object.__setattr__(self, "route_ready_entries", route_ready_entries)
        object.__setattr__(self, "dashboard_visible_entries", dashboard_visible_entries)

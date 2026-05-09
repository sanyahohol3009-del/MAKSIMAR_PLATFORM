from __future__ import annotations

import re
from dataclasses import dataclass


_VIEW_ID_PATTERN = re.compile(r"^view_memory_[a-z][a-z0-9_]*$")


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
class MemoryRegistryViewEntry:
    view_id: str
    panel_id: str
    source_component: str
    source_ref: str
    visible_count: int
    read_only: bool
    preview_ready: bool
    dashboard_visible: bool

    def __post_init__(self) -> None:
        view_id = _ensure_non_empty_str(self.view_id, "view_id")
        panel_id = _ensure_non_empty_str(self.panel_id, "panel_id")
        source_component = _ensure_non_empty_str(
            self.source_component,
            "source_component",
        )
        source_ref = _ensure_non_empty_str(self.source_ref, "source_ref")
        visible_count = _ensure_non_negative_int(self.visible_count, "visible_count")

        if not _VIEW_ID_PATTERN.fullmatch(view_id):
            raise ValueError(f"Invalid view_id: {view_id}")
        if not panel_id.startswith("panel_memory_"):
            raise ValueError(f"Invalid panel_id: {panel_id}")

        for field_name in ("read_only", "preview_ready", "dashboard_visible"):
            _ensure_bool(getattr(self, field_name), field_name)

        if not self.read_only:
            raise ValueError("read_only must be True")
        if not self.preview_ready:
            raise ValueError("preview_ready must be True")
        if not self.dashboard_visible:
            raise ValueError("dashboard_visible must be True")

        object.__setattr__(self, "view_id", view_id)
        object.__setattr__(self, "panel_id", panel_id)
        object.__setattr__(self, "source_component", source_component)
        object.__setattr__(self, "source_ref", source_ref)
        object.__setattr__(self, "visible_count", visible_count)


@dataclass(frozen=True, slots=True)
class MemoryRegistryViewContract:
    total_views: int
    read_only_views: int
    preview_ready_views: int
    dashboard_visible_views: int
    entries: tuple[MemoryRegistryViewEntry, ...]

    def __post_init__(self) -> None:
        total_views = _ensure_non_negative_int(self.total_views, "total_views")
        read_only_views = _ensure_non_negative_int(self.read_only_views, "read_only_views")
        preview_ready_views = _ensure_non_negative_int(
            self.preview_ready_views,
            "preview_ready_views",
        )
        dashboard_visible_views = _ensure_non_negative_int(
            self.dashboard_visible_views,
            "dashboard_visible_views",
        )

        if total_views != len(self.entries):
            raise ValueError("total_views must match entries length")
        if total_views <= 0:
            raise ValueError("total_views must be >= 1")
        if read_only_views != sum(1 for entry in self.entries if entry.read_only):
            raise ValueError("read_only_views must match computed count")
        if preview_ready_views != sum(1 for entry in self.entries if entry.preview_ready):
            raise ValueError("preview_ready_views must match computed count")
        if dashboard_visible_views != sum(
            1 for entry in self.entries if entry.dashboard_visible
        ):
            raise ValueError("dashboard_visible_views must match computed count")

        if read_only_views != total_views:
            raise ValueError("all views must be read-only")
        if preview_ready_views != total_views:
            raise ValueError("all views must be preview-ready")
        if dashboard_visible_views != total_views:
            raise ValueError("all views must be dashboard-visible")

        view_ids = tuple(entry.view_id for entry in self.entries)
        if len(set(view_ids)) != len(view_ids):
            raise ValueError("duplicate view_id values detected")

        object.__setattr__(self, "total_views", total_views)
        object.__setattr__(self, "read_only_views", read_only_views)
        object.__setattr__(self, "preview_ready_views", preview_ready_views)
        object.__setattr__(self, "dashboard_visible_views", dashboard_visible_views)

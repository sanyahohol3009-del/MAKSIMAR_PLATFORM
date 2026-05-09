from __future__ import annotations

import re
from dataclasses import dataclass
from typing import Literal


DashboardReadOnlyViewKind = Literal[
    "memory_dashboard_view",
    "skill_dashboard_view",
    "memory_registry_read_only_view",
]

DashboardReadOnlyViewId = Literal[
    "view_memory_project_architecture",
    "view_simulation_skill_overview",
    "view_memory_domain_map",
    "view_memory_registry_graph",
    "view_memory_timeline",
    "view_memory_retrieval_trace",
    "view_memory_storage_map",
    "view_memory_media_artifact_flow",
    "view_memory_model_store_status",
    "view_memory_history_flow",
]

DashboardReadOnlyDisplayRole = Literal[
    "mobile_display_proxy",
    "engineering_display",
]

DashboardReadOnlyMode = Literal[
    "read_only",
]


_VIEW_ENTRY_ID_PATTERN = re.compile(r"^dashboardview_[a-z][a-z0-9_]*$")
_MEMORY_TIER_ID_PATTERN = re.compile(r"^memory_[a-z][a-z0-9_]*$")
_SKILL_ID_PATTERN = re.compile(r"^skill_[a-z][a-z0-9_]*_[a-z][a-z0-9_]*$")
_METRIC_ID_PATTERN = re.compile(r"^(msmetric|pdmetric)_[a-z][a-z0-9_]*$")
_DISPLAY_ID_PATTERN = re.compile(r"^display_[a-z][a-z0-9_]*$")
_PANEL_ID_PATTERN = re.compile(r"^panel_[a-z][a-z0-9_]*$")

_MEMORY_REGISTRY_VIEW_IDS = {
    "view_memory_domain_map",
    "view_memory_registry_graph",
    "view_memory_timeline",
    "view_memory_retrieval_trace",
    "view_memory_storage_map",
    "view_memory_media_artifact_flow",
    "view_memory_model_store_status",
    "view_memory_history_flow",
}


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
class DashboardReadOnlyViewEntry:
    """Canonical dashboard read-only view entry for memory/skill exposure."""

    view_entry_id: str
    view_kind: DashboardReadOnlyViewKind
    view_id: DashboardReadOnlyViewId
    linked_memory_tier_id: str
    linked_skill_id: str
    linked_metric_id: str
    display_id: str
    display_role: DashboardReadOnlyDisplayRole
    panel_id: str
    read_only_mode: DashboardReadOnlyMode
    multilingual_ready: bool
    explanation_available: bool
    active: bool
    description: str

    def __post_init__(self) -> None:
        """Validate dashboard read-only view invariants."""

        view_entry_id = _ensure_non_empty_str(self.view_entry_id, "view_entry_id")
        linked_metric_id = _ensure_non_empty_str(
            self.linked_metric_id,
            "linked_metric_id",
        )
        display_id = _ensure_non_empty_str(self.display_id, "display_id")
        panel_id = _ensure_non_empty_str(self.panel_id, "panel_id")
        description = _ensure_non_empty_str(self.description, "description")

        if not _VIEW_ENTRY_ID_PATTERN.fullmatch(view_entry_id):
            raise ValueError(f"Invalid view_entry_id: {view_entry_id}")
        if not _METRIC_ID_PATTERN.fullmatch(linked_metric_id):
            raise ValueError(f"Invalid linked_metric_id: {linked_metric_id}")
        if not _DISPLAY_ID_PATTERN.fullmatch(display_id):
            raise ValueError(f"Invalid display_id: {display_id}")
        if not _PANEL_ID_PATTERN.fullmatch(panel_id):
            raise ValueError(f"Invalid panel_id: {panel_id}")

        _ensure_bool(self.multilingual_ready, "multilingual_ready")
        _ensure_bool(self.explanation_available, "explanation_available")
        _ensure_bool(self.active, "active")

        if self.read_only_mode != "read_only":
            raise ValueError(
                f"dashboard memory/skill views must be read-only: {view_entry_id}"
            )
        if not self.multilingual_ready:
            raise ValueError(f"dashboard view must be multilingual-ready: {view_entry_id}")
        if not self.explanation_available:
            raise ValueError(f"dashboard view must expose explanation: {view_entry_id}")
        if not self.active:
            raise ValueError(f"dashboard view must target active bindings: {view_entry_id}")

        if self.view_kind == "memory_dashboard_view":
            self._validate_memory_dashboard_view(view_entry_id)
        elif self.view_kind == "skill_dashboard_view":
            self._validate_skill_dashboard_view(view_entry_id)
        elif self.view_kind == "memory_registry_read_only_view":
            self._validate_memory_registry_read_only_view(view_entry_id)
        else:
            raise ValueError(f"Unsupported view_kind: {self.view_kind}")

        object.__setattr__(self, "view_entry_id", view_entry_id)
        object.__setattr__(self, "linked_metric_id", linked_metric_id)
        object.__setattr__(self, "display_id", display_id)
        object.__setattr__(self, "panel_id", panel_id)
        object.__setattr__(self, "description", description)

    def _validate_memory_dashboard_view(self, view_entry_id: str) -> None:
        if self.view_id != "view_memory_project_architecture":
            raise ValueError(
                f"memory_dashboard_view must use view_memory_project_architecture: {view_entry_id}"
            )
        if not _MEMORY_TIER_ID_PATTERN.fullmatch(self.linked_memory_tier_id):
            raise ValueError(
                f"memory_dashboard_view must define linked_memory_tier_id: {view_entry_id}"
            )
        if self.linked_skill_id != "":
            raise ValueError(
                f"memory_dashboard_view must not define linked_skill_id: {view_entry_id}"
            )
        if self.display_role != "mobile_display_proxy":
            raise ValueError(
                f"memory_dashboard_view must bind to mobile_display_proxy: {view_entry_id}"
            )
        if self.panel_id != "panel_memory_project_architecture":
            raise ValueError(
                f"memory_dashboard_view must bind to panel_memory_project_architecture: {view_entry_id}"
            )

    def _validate_skill_dashboard_view(self, view_entry_id: str) -> None:
        if self.view_id != "view_simulation_skill_overview":
            raise ValueError(
                f"skill_dashboard_view must use view_simulation_skill_overview: {view_entry_id}"
            )
        if self.linked_memory_tier_id != "":
            raise ValueError(
                f"skill_dashboard_view must not define linked_memory_tier_id: {view_entry_id}"
            )
        if not _SKILL_ID_PATTERN.fullmatch(self.linked_skill_id):
            raise ValueError(
                f"skill_dashboard_view must define linked_skill_id: {view_entry_id}"
            )
        if self.display_role != "engineering_display":
            raise ValueError(
                f"skill_dashboard_view must bind to engineering_display: {view_entry_id}"
            )
        if self.panel_id != "panel_simulation_skill_overview":
            raise ValueError(
                f"skill_dashboard_view must bind to panel_simulation_skill_overview: {view_entry_id}"
            )

    def _validate_memory_registry_read_only_view(self, view_entry_id: str) -> None:
        if self.view_id not in _MEMORY_REGISTRY_VIEW_IDS:
            raise ValueError(f"Invalid memory registry read-only view_id: {view_entry_id}")
        if not _MEMORY_TIER_ID_PATTERN.fullmatch(self.linked_memory_tier_id):
            raise ValueError(
                f"memory_registry_read_only_view must define linked_memory_tier_id: {view_entry_id}"
            )
        if self.linked_skill_id != "":
            raise ValueError(
                f"memory_registry_read_only_view must not define linked_skill_id: {view_entry_id}"
            )
        if self.display_role != "mobile_display_proxy":
            raise ValueError(
                f"memory_registry_read_only_view must bind to mobile_display_proxy: {view_entry_id}"
            )
        if not self.panel_id.startswith("panel_memory_"):
            raise ValueError(
                f"memory_registry_read_only_view must bind to memory panel: {view_entry_id}"
            )


@dataclass(frozen=True, slots=True)
class DashboardReadOnlyViewsContract:
    """Unified dashboard read-only memory/skill views contract."""

    total_entries: int
    active_entries: int
    multilingual_ready_entries: int
    explanation_available_entries: int
    entries: tuple[DashboardReadOnlyViewEntry, ...]

    def __post_init__(self) -> None:
        """Validate dashboard read-only views contract invariants."""

        total_entries = _ensure_non_negative_int(self.total_entries, "total_entries")
        active_entries = _ensure_non_negative_int(self.active_entries, "active_entries")
        multilingual_ready_entries = _ensure_non_negative_int(
            self.multilingual_ready_entries,
            "multilingual_ready_entries",
        )
        explanation_available_entries = _ensure_non_negative_int(
            self.explanation_available_entries,
            "explanation_available_entries",
        )

        if total_entries != len(self.entries):
            raise ValueError("total_entries must match entries length")

        computed_active_entries = sum(1 for entry in self.entries if entry.active)
        computed_multilingual_ready_entries = sum(
            1 for entry in self.entries if entry.multilingual_ready
        )
        computed_explanation_available_entries = sum(
            1 for entry in self.entries if entry.explanation_available
        )

        if active_entries != computed_active_entries:
            raise ValueError("active_entries must match computed count")
        if multilingual_ready_entries != computed_multilingual_ready_entries:
            raise ValueError("multilingual_ready_entries must match computed count")
        if explanation_available_entries != computed_explanation_available_entries:
            raise ValueError("explanation_available_entries must match computed count")

        view_entry_ids = tuple(entry.view_entry_id for entry in self.entries)
        view_ids = tuple(entry.view_id for entry in self.entries)

        if len(set(view_entry_ids)) != len(view_entry_ids):
            raise ValueError("Duplicate view_entry_id values detected")
        if len(set(view_ids)) != len(view_ids):
            raise ValueError("Duplicate view_id values detected")

        if not self.entries:
            raise ValueError("dashboard read-only views contract must contain entries")

        object.__setattr__(self, "total_entries", total_entries)
        object.__setattr__(self, "active_entries", active_entries)
        object.__setattr__(
            self,
            "multilingual_ready_entries",
            multilingual_ready_entries,
        )
        object.__setattr__(
            self,
            "explanation_available_entries",
            explanation_available_entries,
        )

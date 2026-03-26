from __future__ import annotations

import re
from dataclasses import dataclass
from typing import Literal


DashboardReadOnlyViewKind = Literal[
    "memory_dashboard_view",
    "skill_dashboard_view",
]

DashboardReadOnlyViewId = Literal[
    "view_memory_project_architecture",
    "view_simulation_skill_overview",
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
        if not _VIEW_ENTRY_ID_PATTERN.fullmatch(self.view_entry_id):
            raise ValueError(f"Invalid view_entry_id: {self.view_entry_id}")

        if not _METRIC_ID_PATTERN.fullmatch(self.linked_metric_id):
            raise ValueError(f"Invalid linked_metric_id: {self.linked_metric_id}")

        if not _DISPLAY_ID_PATTERN.fullmatch(self.display_id):
            raise ValueError(f"Invalid display_id: {self.display_id}")

        if not _PANEL_ID_PATTERN.fullmatch(self.panel_id):
            raise ValueError(f"Invalid panel_id: {self.panel_id}")

        if not self.description.strip():
            raise ValueError(f"description must not be empty: {self.view_entry_id}")

        if self.read_only_mode != "read_only":
            raise ValueError(
                f"dashboard memory/skill views must be read-only: {self.view_entry_id}"
            )

        if not self.multilingual_ready:
            raise ValueError(
                f"dashboard view must be multilingual-ready: {self.view_entry_id}"
            )

        if not self.explanation_available:
            raise ValueError(
                f"dashboard view must expose explanation: {self.view_entry_id}"
            )

        if not self.active:
            raise ValueError(
                f"dashboard view must target active bindings: {self.view_entry_id}"
            )

        if self.view_kind == "memory_dashboard_view":
            if self.view_id != "view_memory_project_architecture":
                raise ValueError(
                    f"memory_dashboard_view must use view_memory_project_architecture: {self.view_entry_id}"
                )
            if not _MEMORY_TIER_ID_PATTERN.fullmatch(self.linked_memory_tier_id):
                raise ValueError(
                    f"memory_dashboard_view must define linked_memory_tier_id: {self.view_entry_id}"
                )
            if self.linked_skill_id != "":
                raise ValueError(
                    f"memory_dashboard_view must not define linked_skill_id: {self.view_entry_id}"
                )
            if self.display_role != "mobile_display_proxy":
                raise ValueError(
                    f"memory_dashboard_view must bind to mobile_display_proxy: {self.view_entry_id}"
                )
            if self.panel_id != "panel_memory_project_architecture":
                raise ValueError(
                    f"memory_dashboard_view must bind to panel_memory_project_architecture: {self.view_entry_id}"
                )

        if self.view_kind == "skill_dashboard_view":
            if self.view_id != "view_simulation_skill_overview":
                raise ValueError(
                    f"skill_dashboard_view must use view_simulation_skill_overview: {self.view_entry_id}"
                )
            if self.linked_memory_tier_id != "":
                raise ValueError(
                    f"skill_dashboard_view must not define linked_memory_tier_id: {self.view_entry_id}"
                )
            if not _SKILL_ID_PATTERN.fullmatch(self.linked_skill_id):
                raise ValueError(
                    f"skill_dashboard_view must define linked_skill_id: {self.view_entry_id}"
                )
            if self.display_role != "engineering_display":
                raise ValueError(
                    f"skill_dashboard_view must bind to engineering_display: {self.view_entry_id}"
                )
            if self.panel_id != "panel_simulation_skill_overview":
                raise ValueError(
                    f"skill_dashboard_view must bind to panel_simulation_skill_overview: {self.view_entry_id}"
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
        if self.total_entries != len(self.entries):
            raise ValueError("total_entries must match entries length")

        active_entries = sum(1 for entry in self.entries if entry.active)
        multilingual_ready_entries = sum(
            1 for entry in self.entries if entry.multilingual_ready
        )
        explanation_available_entries = sum(
            1 for entry in self.entries if entry.explanation_available
        )

        if self.active_entries != active_entries:
            raise ValueError("active_entries must match computed count")

        if self.multilingual_ready_entries != multilingual_ready_entries:
            raise ValueError("multilingual_ready_entries must match computed count")

        if self.explanation_available_entries != explanation_available_entries:
            raise ValueError("explanation_available_entries must match computed count")

        view_entry_ids = tuple(entry.view_entry_id for entry in self.entries)
        view_ids = tuple(entry.view_id for entry in self.entries)

        if len(set(view_entry_ids)) != len(view_entry_ids):
            raise ValueError("Duplicate view_entry_id values detected")

        if len(set(view_ids)) != len(view_ids):
            raise ValueError("Duplicate view_id values detected")

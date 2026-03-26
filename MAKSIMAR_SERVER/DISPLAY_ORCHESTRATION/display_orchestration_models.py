from __future__ import annotations

import re
from dataclasses import dataclass
from typing import Literal


DisplayCommandIntent = Literal[
    "show_memory",
    "show_simulation",
    "show_monitoring",
]

DisplayViewId = Literal[
    "view_memory_project_architecture",
    "view_simulation_skill_overview",
    "view_monitoring_panel",
]

DisplayTargetRole = Literal[
    "primary_dashboard_display",
    "engineering_display",
    "mobile_display_proxy",
]

DisplayRouteStatus = Literal[
    "routed",
]

_ROUTE_REQUEST_ID_PATTERN = re.compile(r"^displayroute_[a-z][a-z0-9_]*$")
_DISPLAY_ID_PATTERN = re.compile(r"^display_[a-z][a-z0-9_]*$")
_ZONE_ID_PATTERN = re.compile(r"^zone_[a-z][a-z0-9_]*$")
_PANEL_ID_PATTERN = re.compile(r"^panel_[a-z][a-z0-9_]*$")


@dataclass(frozen=True, slots=True)
class DisplayOrchestrationEntry:
    """Canonical display orchestration entry."""

    route_request_id: str
    command_intent: DisplayCommandIntent
    resolved_view_id: DisplayViewId
    selected_display_id: str
    selected_display_role: DisplayTargetRole
    selected_zone_id: str
    selected_panel_id: str
    explanation_required: bool
    registry_routed: bool
    multilingual_ready: bool
    route_status: DisplayRouteStatus
    description: str

    def __post_init__(self) -> None:
        """Validate display orchestration invariants."""
        if not _ROUTE_REQUEST_ID_PATTERN.fullmatch(self.route_request_id):
            raise ValueError(f"Invalid route_request_id: {self.route_request_id}")

        if not _DISPLAY_ID_PATTERN.fullmatch(self.selected_display_id):
            raise ValueError(f"Invalid selected_display_id: {self.selected_display_id}")

        if not _ZONE_ID_PATTERN.fullmatch(self.selected_zone_id):
            raise ValueError(f"Invalid selected_zone_id: {self.selected_zone_id}")

        if not _PANEL_ID_PATTERN.fullmatch(self.selected_panel_id):
            raise ValueError(f"Invalid selected_panel_id: {self.selected_panel_id}")

        if not self.description.strip():
            raise ValueError(
                f"description must not be empty for {self.route_request_id}"
            )

        if not self.explanation_required:
            raise ValueError(
                f"display orchestration must require explanation: {self.route_request_id}"
            )

        if not self.registry_routed:
            raise ValueError(
                f"display orchestration must be registry-routed: {self.route_request_id}"
            )

        if not self.multilingual_ready:
            raise ValueError(
                f"display orchestration must be multilingual-ready: {self.route_request_id}"
            )

        if self.route_status != "routed":
            raise ValueError(
                f"display orchestration entry must be routed: {self.route_request_id}"
            )

        if self.command_intent == "show_memory":
            if self.resolved_view_id != "view_memory_project_architecture":
                raise ValueError(
                    f"show_memory must resolve to view_memory_project_architecture: {self.route_request_id}"
                )
            if self.selected_panel_id != "panel_memory_project_architecture":
                raise ValueError(
                    f"show_memory must route to panel_memory_project_architecture: {self.route_request_id}"
                )

        if self.command_intent == "show_simulation":
            if self.resolved_view_id != "view_simulation_skill_overview":
                raise ValueError(
                    f"show_simulation must resolve to view_simulation_skill_overview: {self.route_request_id}"
                )
            if self.selected_panel_id != "panel_simulation_skill_overview":
                raise ValueError(
                    f"show_simulation must route to panel_simulation_skill_overview: {self.route_request_id}"
                )

        if self.command_intent == "show_monitoring":
            if self.resolved_view_id != "view_monitoring_panel":
                raise ValueError(
                    f"show_monitoring must resolve to view_monitoring_panel: {self.route_request_id}"
                )
            if self.selected_panel_id != "panel_monitoring_panel":
                raise ValueError(
                    f"show_monitoring must route to panel_monitoring_panel: {self.route_request_id}"
                )

        if self.selected_display_role == "mobile_display_proxy":
            if self.command_intent != "show_memory":
                raise ValueError(
                    f"mobile_display_proxy is reserved for show_memory in current topology: {self.route_request_id}"
                )


@dataclass(frozen=True, slots=True)
class DisplayOrchestrationContract:
    """Unified display orchestration contract."""

    total_entries: int
    explanation_required_entries: int
    registry_routed_entries: int
    multilingual_ready_entries: int
    entries: tuple[DisplayOrchestrationEntry, ...]

    def __post_init__(self) -> None:
        """Validate display orchestration contract invariants."""
        if self.total_entries != len(self.entries):
            raise ValueError("total_entries must match entries length")

        explanation_required_entries = sum(
            1 for entry in self.entries if entry.explanation_required
        )
        registry_routed_entries = sum(
            1 for entry in self.entries if entry.registry_routed
        )
        multilingual_ready_entries = sum(
            1 for entry in self.entries if entry.multilingual_ready
        )

        if self.explanation_required_entries != explanation_required_entries:
            raise ValueError(
                "explanation_required_entries must match computed count"
            )

        if self.registry_routed_entries != registry_routed_entries:
            raise ValueError("registry_routed_entries must match computed count")

        if self.multilingual_ready_entries != multilingual_ready_entries:
            raise ValueError("multilingual_ready_entries must match computed count")

        route_request_ids = tuple(entry.route_request_id for entry in self.entries)
        if len(set(route_request_ids)) != len(route_request_ids):
            raise ValueError("Duplicate route_request_id values detected")

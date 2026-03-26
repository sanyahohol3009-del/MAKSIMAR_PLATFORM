from __future__ import annotations

import re
from dataclasses import dataclass
from typing import Literal


PresentationDisplayMetricSource = Literal[
    "display_orchestration",
]

PresentationDisplayViewId = Literal[
    "view_memory_project_architecture",
    "view_simulation_skill_overview",
    "view_monitoring_panel",
]

PresentationDisplayRole = Literal[
    "mobile_display_proxy",
    "engineering_display",
    "primary_dashboard_display",
]

PresentationDisplayVisibilityMode = Literal[
    "private",
    "shared",
]

PresentationDisplaySeverity = Literal[
    "info",
    "warning",
    "critical",
]


_METRIC_ID_PATTERN = re.compile(r"^pdmetric_[a-z][a-z0-9_]*$")
_ROUTE_REQUEST_ID_PATTERN = re.compile(r"^displayroute_[a-z][a-z0-9_]*$")
_DISPLAY_ID_PATTERN = re.compile(r"^display_[a-z][a-z0-9_]*$")
_ZONE_ID_PATTERN = re.compile(r"^zone_[a-z][a-z0-9_]*$")
_PANEL_ID_PATTERN = re.compile(r"^panel_[a-z][a-z0-9_]*$")


@dataclass(frozen=True, slots=True)
class PresentationDisplayMetricEntry:
    """Canonical observability metric entry for presentation/display routing."""

    metric_id: str
    source_component: PresentationDisplayMetricSource
    route_request_id: str
    view_id: PresentationDisplayViewId
    display_id: str
    display_role: PresentationDisplayRole
    zone_id: str
    panel_id: str
    visibility_mode: PresentationDisplayVisibilityMode
    explanation_bound: bool
    multilingual_ready: bool
    registry_routed: bool
    event_severity: PresentationDisplaySeverity
    alert_emitted: bool
    description: str

    def __post_init__(self) -> None:
        """Validate presentation/display metric invariants."""
        if not _METRIC_ID_PATTERN.fullmatch(self.metric_id):
            raise ValueError(f"Invalid metric_id: {self.metric_id}")

        if not _ROUTE_REQUEST_ID_PATTERN.fullmatch(self.route_request_id):
            raise ValueError(f"Invalid route_request_id: {self.route_request_id}")

        if not _DISPLAY_ID_PATTERN.fullmatch(self.display_id):
            raise ValueError(f"Invalid display_id: {self.display_id}")

        if not _ZONE_ID_PATTERN.fullmatch(self.zone_id):
            raise ValueError(f"Invalid zone_id: {self.zone_id}")

        if not _PANEL_ID_PATTERN.fullmatch(self.panel_id):
            raise ValueError(f"Invalid panel_id: {self.panel_id}")

        if not self.description.strip():
            raise ValueError(f"description must not be empty: {self.metric_id}")

        if self.source_component != "display_orchestration":
            raise ValueError(
                f"presentation/display metric must use display_orchestration source: {self.metric_id}"
            )

        if not self.explanation_bound:
            raise ValueError(
                f"presentation/display metric must be explanation-bound: {self.metric_id}"
            )

        if not self.multilingual_ready:
            raise ValueError(
                f"presentation/display metric must be multilingual-ready: {self.metric_id}"
            )

        if not self.registry_routed:
            raise ValueError(
                f"presentation/display metric must be registry-routed: {self.metric_id}"
            )

        if self.event_severity != "info":
            raise ValueError(
                f"presentation/display metric must use severity='info': {self.metric_id}"
            )

        if self.alert_emitted:
            raise ValueError(
                f"presentation/display metric must not emit alerts: {self.metric_id}"
            )

        if self.view_id == "view_memory_project_architecture":
            if self.panel_id != "panel_memory_project_architecture":
                raise ValueError(
                    f"view_memory_project_architecture must bind to panel_memory_project_architecture: {self.metric_id}"
                )
            if self.display_role != "mobile_display_proxy":
                raise ValueError(
                    f"view_memory_project_architecture must bind to mobile_display_proxy: {self.metric_id}"
                )

        if self.view_id == "view_simulation_skill_overview":
            if self.panel_id != "panel_simulation_skill_overview":
                raise ValueError(
                    f"view_simulation_skill_overview must bind to panel_simulation_skill_overview: {self.metric_id}"
                )
            if self.display_role != "engineering_display":
                raise ValueError(
                    f"view_simulation_skill_overview must bind to engineering_display: {self.metric_id}"
                )

        if self.view_id == "view_monitoring_panel":
            if self.panel_id != "panel_monitoring_panel":
                raise ValueError(
                    f"view_monitoring_panel must bind to panel_monitoring_panel: {self.metric_id}"
                )
            if self.display_role != "primary_dashboard_display":
                raise ValueError(
                    f"view_monitoring_panel must bind to primary_dashboard_display: {self.metric_id}"
                )

        if self.display_role == "mobile_display_proxy":
            if self.visibility_mode != "private":
                raise ValueError(
                    f"mobile_display_proxy must use private visibility: {self.metric_id}"
                )

        if self.display_role in (
            "engineering_display",
            "primary_dashboard_display",
        ):
            if self.visibility_mode != "shared":
                raise ValueError(
                    f"shared display roles must use shared visibility: {self.metric_id}"
                )


@dataclass(frozen=True, slots=True)
class PresentationDisplayMetricsContract:
    """Unified observability contract for presentation/display routing."""

    total_entries: int
    private_route_entries: int
    shared_route_entries: int
    explanation_bound_entries: int
    multilingual_ready_entries: int
    entries: tuple[PresentationDisplayMetricEntry, ...]

    def __post_init__(self) -> None:
        """Validate presentation/display metrics contract invariants."""
        if self.total_entries != len(self.entries):
            raise ValueError("total_entries must match entries length")

        private_route_entries = sum(
            1 for entry in self.entries if entry.visibility_mode == "private"
        )
        shared_route_entries = sum(
            1 for entry in self.entries if entry.visibility_mode == "shared"
        )
        explanation_bound_entries = sum(
            1 for entry in self.entries if entry.explanation_bound
        )
        multilingual_ready_entries = sum(
            1 for entry in self.entries if entry.multilingual_ready
        )

        if self.private_route_entries != private_route_entries:
            raise ValueError("private_route_entries must match computed count")

        if self.shared_route_entries != shared_route_entries:
            raise ValueError("shared_route_entries must match computed count")

        if self.explanation_bound_entries != explanation_bound_entries:
            raise ValueError("explanation_bound_entries must match computed count")

        if self.multilingual_ready_entries != multilingual_ready_entries:
            raise ValueError("multilingual_ready_entries must match computed count")

        metric_ids = tuple(entry.metric_id for entry in self.entries)
        route_request_ids = tuple(entry.route_request_id for entry in self.entries)

        if len(set(metric_ids)) != len(metric_ids):
            raise ValueError("Duplicate metric_id values detected")

        if len(set(route_request_ids)) != len(route_request_ids):
            raise ValueError("Duplicate route_request_id values detected")

from __future__ import annotations

import re
from dataclasses import dataclass
from typing import Literal

from MAKSIMAR_SERVER.DASHBOARD_READ_ONLY_VIEWS import (
    build_dashboard_read_only_views_contract,
)
from MAKSIMAR_SERVER.DISPLAY_ORCHESTRATION import (
    build_display_orchestration_contract,
)
from MAKSIMAR_SERVER.DISPLAY_ORCHESTRATION.memory_presentation.presentation_request_models import (
    build_presentation_request_contract,
)

ViewResolutionSource = Literal[
    "dashboard_read_only_view",
    "display_orchestration_route",
]

_VIEW_RESOLUTION_ID_PATTERN = re.compile(r"^view_resolution_[a-z][a-z0-9_]*_[0-9]{3}$")


def _ensure_non_empty_str(value: str, field_name: str) -> str:
    if not isinstance(value, str):
        raise ValueError(f"{field_name} must be a string")
    normalized = value.strip()
    if not normalized:
        raise ValueError(f"{field_name} must be a non-empty string")
    return normalized


def _ensure_bool(value: bool, field_name: str) -> bool:
    if not isinstance(value, bool):
        raise ValueError(f"{field_name} must be bool")
    return value


@dataclass(frozen=True, slots=True)
class ViewResolutionEntry:
    view_resolution_id: str
    presentation_request_id: str
    command_intent: str
    requested_view_hint: str
    resolved_view_id: str
    resolved_view_kind: str
    resolved_panel_id: str
    resolution_source: ViewResolutionSource
    dashboard_view_bound: bool
    source_bound: bool
    explanation_available: bool
    multilingual_ready: bool
    read_only: bool
    resolution_ready: bool
    description: str

    def __post_init__(self) -> None:
        resolution_id = _ensure_non_empty_str(
            self.view_resolution_id,
            "view_resolution_id",
        )
        if not _VIEW_RESOLUTION_ID_PATTERN.fullmatch(resolution_id):
            raise ValueError(f"Invalid view_resolution_id: {resolution_id}")

        for field_name in (
            "presentation_request_id",
            "command_intent",
            "requested_view_hint",
            "resolved_view_id",
            "resolved_view_kind",
            "resolved_panel_id",
            "description",
        ):
            _ensure_non_empty_str(getattr(self, field_name), field_name)

        for field_name in (
            "dashboard_view_bound",
            "source_bound",
            "explanation_available",
            "multilingual_ready",
            "read_only",
            "resolution_ready",
        ):
            _ensure_bool(getattr(self, field_name), field_name)

        if not self.source_bound:
            raise ValueError("source_bound must be True")
        if not self.explanation_available:
            raise ValueError("explanation_available must be True")
        if not self.multilingual_ready:
            raise ValueError("multilingual_ready must be True")
        if not self.read_only:
            raise ValueError("read_only must be True")
        if not self.resolution_ready:
            raise ValueError("resolution_ready must be True")


@dataclass(frozen=True, slots=True)
class ViewResolutionContract:
    total_resolutions: int
    ready_resolutions: int
    dashboard_bound_resolutions: int
    source_bound_resolutions: int
    explanation_available_resolutions: int
    multilingual_ready_resolutions: int
    read_only_resolutions: int
    entries: tuple[ViewResolutionEntry, ...]

    def __post_init__(self) -> None:
        if self.total_resolutions != len(self.entries):
            raise ValueError("total_resolutions must match entries length")
        if self.total_resolutions <= 0:
            raise ValueError("total_resolutions must be >= 1")

        expected = {
            "ready_resolutions": sum(1 for entry in self.entries if entry.resolution_ready),
            "dashboard_bound_resolutions": sum(1 for entry in self.entries if entry.dashboard_view_bound),
            "source_bound_resolutions": sum(1 for entry in self.entries if entry.source_bound),
            "explanation_available_resolutions": sum(1 for entry in self.entries if entry.explanation_available),
            "multilingual_ready_resolutions": sum(1 for entry in self.entries if entry.multilingual_ready),
            "read_only_resolutions": sum(1 for entry in self.entries if entry.read_only),
        }

        for field_name, expected_value in expected.items():
            if getattr(self, field_name) != expected_value:
                raise ValueError(f"{field_name} must match computed count")

        if self.ready_resolutions != self.total_resolutions:
            raise ValueError("all view resolutions must be ready")
        if self.source_bound_resolutions != self.total_resolutions:
            raise ValueError("all view resolutions must be source-bound")
        if self.explanation_available_resolutions != self.total_resolutions:
            raise ValueError("all view resolutions must have explanation")
        if self.multilingual_ready_resolutions != self.total_resolutions:
            raise ValueError("all view resolutions must be multilingual-ready")
        if self.read_only_resolutions != self.total_resolutions:
            raise ValueError("all view resolutions must be read-only")


def build_view_resolution_contract() -> ViewResolutionContract:
    requests = build_presentation_request_contract()
    dashboard = build_dashboard_read_only_views_contract()
    orchestration = build_display_orchestration_contract()

    dashboard_by_view_id = {entry.view_id: entry for entry in dashboard.entries}
    route_by_intent = {entry.command_intent: entry for entry in orchestration.entries}

    entries: list[ViewResolutionEntry] = []

    for request in requests.entries:
        route = route_by_intent.get(request.command_intent)
        if route is None:
            raise ValueError(f"No display orchestration route for {request.command_intent}")

        dashboard_view = dashboard_by_view_id.get(route.resolved_view_id)

        if dashboard_view is not None:
            entries.append(
                ViewResolutionEntry(
                    view_resolution_id=request.presentation_request_id.replace(
                        "presentation_request_",
                        "view_resolution_",
                        1,
                    ),
                    presentation_request_id=request.presentation_request_id,
                    command_intent=request.command_intent,
                    requested_view_hint=request.requested_view_hint,
                    resolved_view_id=dashboard_view.view_id,
                    resolved_view_kind=dashboard_view.view_kind,
                    resolved_panel_id=dashboard_view.panel_id,
                    resolution_source="dashboard_read_only_view",
                    dashboard_view_bound=True,
                    source_bound=True,
                    explanation_available=dashboard_view.explanation_available,
                    multilingual_ready=dashboard_view.multilingual_ready,
                    read_only=dashboard_view.read_only_mode == "read_only",
                    resolution_ready=(
                        dashboard_view.active
                        and dashboard_view.explanation_available
                        and dashboard_view.multilingual_ready
                        and dashboard_view.read_only_mode == "read_only"
                    ),
                    description=f"Dashboard-bound read-only view resolution for {request.command_intent}.",
                )
            )
            continue

        entries.append(
            ViewResolutionEntry(
                view_resolution_id=request.presentation_request_id.replace(
                    "presentation_request_",
                    "view_resolution_",
                    1,
                ),
                presentation_request_id=request.presentation_request_id,
                command_intent=request.command_intent,
                requested_view_hint=request.requested_view_hint,
                resolved_view_id=route.resolved_view_id,
                resolved_view_kind="display_orchestration_route",
                resolved_panel_id=route.selected_panel_id,
                resolution_source="display_orchestration_route",
                dashboard_view_bound=False,
                source_bound=True,
                explanation_available=route.explanation_required,
                multilingual_ready=route.multilingual_ready,
                read_only=True,
                resolution_ready=(
                    route.route_status == "routed"
                    and route.explanation_required
                    and route.registry_routed
                    and route.multilingual_ready
                ),
                description=f"Route-bound read-only view resolution for {request.command_intent}.",
            )
        )

    contract_entries = tuple(entries)

    return ViewResolutionContract(
        total_resolutions=len(contract_entries),
        ready_resolutions=sum(1 for entry in contract_entries if entry.resolution_ready),
        dashboard_bound_resolutions=sum(1 for entry in contract_entries if entry.dashboard_view_bound),
        source_bound_resolutions=sum(1 for entry in contract_entries if entry.source_bound),
        explanation_available_resolutions=sum(1 for entry in contract_entries if entry.explanation_available),
        multilingual_ready_resolutions=sum(1 for entry in contract_entries if entry.multilingual_ready),
        read_only_resolutions=sum(1 for entry in contract_entries if entry.read_only),
        entries=contract_entries,
    )

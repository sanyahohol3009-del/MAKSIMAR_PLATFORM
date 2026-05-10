from __future__ import annotations

import re
from dataclasses import dataclass
from typing import Literal

from MAKSIMAR_SERVER.DISPLAY_ORCHESTRATION.memory_presentation.display_target_selection_models import (
    build_display_target_selection_contract,
)
from MAKSIMAR_SERVER.DISPLAY_ORCHESTRATION.memory_presentation.panel_resolution_models import (
    build_panel_resolution_contract,
)
from MAKSIMAR_SERVER.DISPLAY_ORCHESTRATION.memory_presentation.presentation_request_models import (
    build_presentation_request_contract,
)
from MAKSIMAR_SERVER.DISPLAY_ORCHESTRATION.memory_presentation.view_resolution_models import (
    build_view_resolution_contract,
)


PresentationRouteStatus = Literal["presentation_ready"]

_PRESENTATION_ROUTE_ID_PATTERN = re.compile(r"^presentation_route_[a-z][a-z0-9_]*_[0-9]{3}$")


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
class PresentationRouteEntry:
    presentation_route_id: str
    presentation_request_id: str
    command_intent: str
    resolved_view_id: str
    resolved_panel_id: str
    selected_display_id: str
    selected_display_role: str
    selected_zone_id: str
    resolution_source: str
    request_bound: bool
    view_bound: bool
    panel_bound: bool
    target_bound: bool
    source_bound: bool
    registry_routed: bool
    read_only: bool
    action_execution_allowed: bool
    direct_display_switching_allowed: bool
    route_status: PresentationRouteStatus
    presentation_ready: bool
    description: str

    def __post_init__(self) -> None:
        route_id = _ensure_non_empty_str(self.presentation_route_id, "presentation_route_id")
        if not _PRESENTATION_ROUTE_ID_PATTERN.fullmatch(route_id):
            raise ValueError(f"Invalid presentation_route_id: {route_id}")

        for field_name in (
            "presentation_request_id",
            "command_intent",
            "resolved_view_id",
            "resolved_panel_id",
            "selected_display_id",
            "selected_display_role",
            "selected_zone_id",
            "resolution_source",
            "description",
        ):
            _ensure_non_empty_str(getattr(self, field_name), field_name)

        for field_name in (
            "request_bound",
            "view_bound",
            "panel_bound",
            "target_bound",
            "source_bound",
            "registry_routed",
            "read_only",
            "action_execution_allowed",
            "direct_display_switching_allowed",
            "presentation_ready",
        ):
            _ensure_bool(getattr(self, field_name), field_name)

        if not self.request_bound:
            raise ValueError("request_bound must be True")
        if not self.view_bound:
            raise ValueError("view_bound must be True")
        if not self.panel_bound:
            raise ValueError("panel_bound must be True")
        if not self.target_bound:
            raise ValueError("target_bound must be True")
        if not self.source_bound:
            raise ValueError("source_bound must be True")
        if not self.registry_routed:
            raise ValueError("registry_routed must be True")
        if not self.read_only:
            raise ValueError("read_only must be True")
        if self.action_execution_allowed:
            raise ValueError("action_execution_allowed must be False")
        if self.direct_display_switching_allowed:
            raise ValueError("direct_display_switching_allowed must be False")
        if self.route_status != "presentation_ready":
            raise ValueError("route_status must be presentation_ready")
        if not self.presentation_ready:
            raise ValueError("presentation_ready must be True")


@dataclass(frozen=True, slots=True)
class PresentationRouterContract:
    total_routes: int
    ready_routes: int
    request_bound_routes: int
    view_bound_routes: int
    panel_bound_routes: int
    target_bound_routes: int
    source_bound_routes: int
    registry_routed_routes: int
    read_only_routes: int
    action_execution_allowed_routes: int
    direct_display_switching_allowed_routes: int
    dashboard_bound_routes: int
    route_bound_routes: int
    entries: tuple[PresentationRouteEntry, ...]

    def __post_init__(self) -> None:
        if self.total_routes != len(self.entries):
            raise ValueError("total_routes must match entries length")
        if self.total_routes <= 0:
            raise ValueError("total_routes must be >= 1")

        expected = {
            "ready_routes": sum(1 for entry in self.entries if entry.presentation_ready),
            "request_bound_routes": sum(1 for entry in self.entries if entry.request_bound),
            "view_bound_routes": sum(1 for entry in self.entries if entry.view_bound),
            "panel_bound_routes": sum(1 for entry in self.entries if entry.panel_bound),
            "target_bound_routes": sum(1 for entry in self.entries if entry.target_bound),
            "source_bound_routes": sum(1 for entry in self.entries if entry.source_bound),
            "registry_routed_routes": sum(1 for entry in self.entries if entry.registry_routed),
            "read_only_routes": sum(1 for entry in self.entries if entry.read_only),
            "action_execution_allowed_routes": sum(1 for entry in self.entries if entry.action_execution_allowed),
            "direct_display_switching_allowed_routes": sum(
                1 for entry in self.entries if entry.direct_display_switching_allowed
            ),
            "dashboard_bound_routes": sum(
                1 for entry in self.entries if entry.resolution_source == "dashboard_read_only_view"
            ),
            "route_bound_routes": sum(
                1 for entry in self.entries if entry.resolution_source == "display_orchestration_route"
            ),
        }

        for field_name, expected_value in expected.items():
            if getattr(self, field_name) != expected_value:
                raise ValueError(f"{field_name} must match computed count")

        if self.ready_routes != self.total_routes:
            raise ValueError("all presentation routes must be ready")
        if self.request_bound_routes != self.total_routes:
            raise ValueError("all routes must be request-bound")
        if self.view_bound_routes != self.total_routes:
            raise ValueError("all routes must be view-bound")
        if self.panel_bound_routes != self.total_routes:
            raise ValueError("all routes must be panel-bound")
        if self.target_bound_routes != self.total_routes:
            raise ValueError("all routes must be target-bound")
        if self.source_bound_routes != self.total_routes:
            raise ValueError("all routes must be source-bound")
        if self.registry_routed_routes != self.total_routes:
            raise ValueError("all routes must be registry-routed")
        if self.read_only_routes != self.total_routes:
            raise ValueError("all routes must be read-only")
        if self.action_execution_allowed_routes != 0:
            raise ValueError("presentation router must not execute actions")
        if self.direct_display_switching_allowed_routes != 0:
            raise ValueError("presentation router must not switch displays directly")
        if self.dashboard_bound_routes <= 0:
            raise ValueError("at least one route must be dashboard-bound")
        if self.route_bound_routes <= 0:
            raise ValueError("at least one route must be route-bound")


def build_presentation_router_contract() -> PresentationRouterContract:
    requests = build_presentation_request_contract()
    views = build_view_resolution_contract()
    panels = build_panel_resolution_contract()
    targets = build_display_target_selection_contract()

    request_by_intent = {entry.command_intent: entry for entry in requests.entries}
    view_by_intent = {entry.command_intent: entry for entry in views.entries}
    panel_by_view_id = {entry.resolved_view_id: entry for entry in panels.entries}
    target_by_panel_id = {entry.selected_panel_id: entry for entry in targets.entries}

    entries: list[PresentationRouteEntry] = []

    for command_intent, request in request_by_intent.items():
        view = view_by_intent[command_intent]
        panel = panel_by_view_id[view.resolved_view_id]
        target = target_by_panel_id[panel.resolved_panel_id]

        route_id = request.presentation_request_id.replace(
            "presentation_request_",
            "presentation_route_",
            1,
        )

        entries.append(
            PresentationRouteEntry(
                presentation_route_id=route_id,
                presentation_request_id=request.presentation_request_id,
                command_intent=command_intent,
                resolved_view_id=view.resolved_view_id,
                resolved_panel_id=panel.resolved_panel_id,
                selected_display_id=target.selected_display_id,
                selected_display_role=target.selected_display_role,
                selected_zone_id=target.selected_zone_id,
                resolution_source=view.resolution_source,
                request_bound=request.request_ready,
                view_bound=view.resolution_ready,
                panel_bound=panel.panel_resolution_ready,
                target_bound=target.target_selection_ready,
                source_bound=view.source_bound and panel.panel_source_bound,
                registry_routed=target.registry_routed,
                read_only=(
                    request.read_only
                    and view.read_only
                    and panel.panel_read_only
                    and target.read_only
                ),
                action_execution_allowed=(
                    request.action_execution_allowed
                    or panel.panel_action_execution_allowed
                ),
                direct_display_switching_allowed=(
                    request.direct_display_switching_allowed
                    or target.direct_display_switching_allowed
                ),
                route_status="presentation_ready",
                presentation_ready=(
                    request.request_ready
                    and view.resolution_ready
                    and panel.panel_resolution_ready
                    and target.target_selection_ready
                    and view.source_bound
                    and panel.panel_source_bound
                    and target.registry_routed
                    and not request.action_execution_allowed
                    and not panel.panel_action_execution_allowed
                    and not request.direct_display_switching_allowed
                    and not target.direct_display_switching_allowed
                ),
                description=f"Read-only presentation route for {command_intent}.",
            )
        )

    contract_entries = tuple(entries)

    return PresentationRouterContract(
        total_routes=len(contract_entries),
        ready_routes=sum(1 for entry in contract_entries if entry.presentation_ready),
        request_bound_routes=sum(1 for entry in contract_entries if entry.request_bound),
        view_bound_routes=sum(1 for entry in contract_entries if entry.view_bound),
        panel_bound_routes=sum(1 for entry in contract_entries if entry.panel_bound),
        target_bound_routes=sum(1 for entry in contract_entries if entry.target_bound),
        source_bound_routes=sum(1 for entry in contract_entries if entry.source_bound),
        registry_routed_routes=sum(1 for entry in contract_entries if entry.registry_routed),
        read_only_routes=sum(1 for entry in contract_entries if entry.read_only),
        action_execution_allowed_routes=sum(
            1 for entry in contract_entries if entry.action_execution_allowed
        ),
        direct_display_switching_allowed_routes=sum(
            1 for entry in contract_entries if entry.direct_display_switching_allowed
        ),
        dashboard_bound_routes=sum(
            1 for entry in contract_entries if entry.resolution_source == "dashboard_read_only_view"
        ),
        route_bound_routes=sum(
            1 for entry in contract_entries if entry.resolution_source == "display_orchestration_route"
        ),
        entries=contract_entries,
    )

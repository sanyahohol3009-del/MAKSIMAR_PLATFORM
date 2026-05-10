from __future__ import annotations

import re
from dataclasses import dataclass

from MAKSIMAR_CORE_LIB.display_topology.display_topology_contract import (
    build_display_topology_contract,
)

_ASSIGNMENT_BINDING_ID_PATTERN = re.compile(r"^display_assignment_binding_[a-z][a-z0-9_]*$")


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
class DisplayAssignmentBindingEntry:
    assignment_binding_id: str
    route_request_id: str
    command_intent: str
    view_id: str
    display_id: str
    display_role: str
    zone_id: str
    panel_id: str
    topology_display_bound: bool
    zone_bound: bool
    panel_bound: bool
    registry_routed: bool
    explanation_required: bool
    multilingual_ready: bool
    read_only: bool
    direct_switching_allowed: bool
    assignment_ready: bool
    description: str

    def __post_init__(self) -> None:
        assignment_binding_id = _ensure_non_empty_str(
            self.assignment_binding_id,
            "assignment_binding_id",
        )
        if not _ASSIGNMENT_BINDING_ID_PATTERN.fullmatch(assignment_binding_id):
            raise ValueError(f"Invalid assignment_binding_id: {assignment_binding_id}")

        for field_name in (
            "route_request_id",
            "command_intent",
            "view_id",
            "display_id",
            "display_role",
            "zone_id",
            "panel_id",
            "description",
        ):
            _ensure_non_empty_str(getattr(self, field_name), field_name)

        for field_name in (
            "topology_display_bound",
            "zone_bound",
            "panel_bound",
            "registry_routed",
            "explanation_required",
            "multilingual_ready",
            "read_only",
            "direct_switching_allowed",
            "assignment_ready",
        ):
            _ensure_bool(getattr(self, field_name), field_name)

        if not self.topology_display_bound:
            raise ValueError("topology_display_bound must be True")
        if not self.zone_bound:
            raise ValueError("zone_bound must be True")
        if not self.panel_bound:
            raise ValueError("panel_bound must be True")
        if not self.registry_routed:
            raise ValueError("registry_routed must be True")
        if not self.explanation_required:
            raise ValueError("explanation_required must be True")
        if not self.multilingual_ready:
            raise ValueError("multilingual_ready must be True")
        if not self.read_only:
            raise ValueError("read_only must be True")
        if self.direct_switching_allowed:
            raise ValueError("direct_switching_allowed must be False")
        if not self.assignment_ready:
            raise ValueError("assignment_ready must be True")


@dataclass(frozen=True, slots=True)
class DisplayAssignmentBindingContract:
    total_assignments: int
    ready_assignments: int
    topology_bound_assignments: int
    zone_bound_assignments: int
    panel_bound_assignments: int
    registry_routed_assignments: int
    read_only_assignments: int
    direct_switching_allowed_assignments: int
    entries: tuple[DisplayAssignmentBindingEntry, ...]

    def __post_init__(self) -> None:
        if self.total_assignments != len(self.entries):
            raise ValueError("total_assignments must match entries length")
        if self.total_assignments <= 0:
            raise ValueError("total_assignments must be >= 1")

        expected = {
            "ready_assignments": sum(1 for entry in self.entries if entry.assignment_ready),
            "topology_bound_assignments": sum(1 for entry in self.entries if entry.topology_display_bound),
            "zone_bound_assignments": sum(1 for entry in self.entries if entry.zone_bound),
            "panel_bound_assignments": sum(1 for entry in self.entries if entry.panel_bound),
            "registry_routed_assignments": sum(1 for entry in self.entries if entry.registry_routed),
            "read_only_assignments": sum(1 for entry in self.entries if entry.read_only),
            "direct_switching_allowed_assignments": sum(
                1 for entry in self.entries if entry.direct_switching_allowed
            ),
        }

        for field_name, expected_value in expected.items():
            if getattr(self, field_name) != expected_value:
                raise ValueError(f"{field_name} must match computed count")

        if self.ready_assignments != self.total_assignments:
            raise ValueError("all display assignments must be ready")
        if self.topology_bound_assignments != self.total_assignments:
            raise ValueError("all display assignments must be topology-bound")
        if self.zone_bound_assignments != self.total_assignments:
            raise ValueError("all display assignments must be zone-bound")
        if self.panel_bound_assignments != self.total_assignments:
            raise ValueError("all display assignments must be panel-bound")
        if self.registry_routed_assignments != self.total_assignments:
            raise ValueError("all display assignments must be registry-routed")
        if self.read_only_assignments != self.total_assignments:
            raise ValueError("all display assignments must be read-only")
        if self.direct_switching_allowed_assignments != 0:
            raise ValueError("display assignments must not allow direct switching")


def build_display_assignment_binding_contract() -> DisplayAssignmentBindingContract:
    from MAKSIMAR_SERVER.DISPLAY_ORCHESTRATION.display_orchestration_contract import (
        build_display_orchestration_contract,
    )

    topology = build_display_topology_contract()
    orchestration = build_display_orchestration_contract()

    display_by_id = {entry.display_id: entry for entry in topology.entries}

    entries = tuple(
        DisplayAssignmentBindingEntry(
            assignment_binding_id=f"display_assignment_binding_{route.route_request_id.removeprefix('displayroute_')}",
            route_request_id=route.route_request_id,
            command_intent=route.command_intent,
            view_id=route.resolved_view_id,
            display_id=route.selected_display_id,
            display_role=route.selected_display_role,
            zone_id=route.selected_zone_id,
            panel_id=route.selected_panel_id,
            topology_display_bound=route.selected_display_id in display_by_id,
            zone_bound=(
                route.selected_display_id in display_by_id
                and route.selected_zone_id in display_by_id[route.selected_display_id].zone_ids
            ),
            panel_bound=(
                route.selected_display_id in display_by_id
                and route.selected_panel_id in display_by_id[route.selected_display_id].default_panel_ids
            ),
            registry_routed=route.registry_routed,
            explanation_required=route.explanation_required,
            multilingual_ready=route.multilingual_ready,
            read_only=True,
            direct_switching_allowed=False,
            assignment_ready=True,
            description=f"Read-only display assignment binding for {route.route_request_id}.",
        )
        for route in orchestration.entries
    )

    return DisplayAssignmentBindingContract(
        total_assignments=len(entries),
        ready_assignments=sum(1 for entry in entries if entry.assignment_ready),
        topology_bound_assignments=sum(1 for entry in entries if entry.topology_display_bound),
        zone_bound_assignments=sum(1 for entry in entries if entry.zone_bound),
        panel_bound_assignments=sum(1 for entry in entries if entry.panel_bound),
        registry_routed_assignments=sum(1 for entry in entries if entry.registry_routed),
        read_only_assignments=sum(1 for entry in entries if entry.read_only),
        direct_switching_allowed_assignments=sum(
            1 for entry in entries if entry.direct_switching_allowed
        ),
        entries=entries,
    )

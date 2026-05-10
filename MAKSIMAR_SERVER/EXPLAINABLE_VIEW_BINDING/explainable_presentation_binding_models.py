from __future__ import annotations

import re
from dataclasses import dataclass
from typing import Any

from MAKSIMAR_SERVER.DISPLAY_ORCHESTRATION.memory_presentation import (
    build_presentation_router_contract,
)
from MAKSIMAR_SERVER.EXPLAINABLE_VIEW_BINDING.explainable_view_binding_contract import (
    build_explainable_view_binding_contract,
)

_BINDING_ID_PATTERN = re.compile(
    r"^explainable_presentation_binding_[a-z][a-z0-9_]*_[0-9]{3}$"
)


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


def _match_explainable_entry(route: object, explainable_entries: tuple[Any, ...]) -> Any:
    route_view_id = getattr(route, "resolved_view_id")
    route_panel_id = getattr(route, "resolved_panel_id")
    route_display_id = getattr(route, "selected_display_id")

    for entry in explainable_entries:
        if (
            entry.view_id == route_view_id
            and entry.panel_id == route_panel_id
            and entry.display_id == route_display_id
        ):
            return entry

    for entry in explainable_entries:
        if entry.view_id == route_view_id and entry.panel_id == route_panel_id:
            return entry

    raise ValueError(
        "No explainable view binding matched presentation route: "
        f"view_id={route_view_id!r}, panel_id={route_panel_id!r}, "
        f"display_id={route_display_id!r}"
    )


@dataclass(frozen=True, slots=True)
class ExplainablePresentationBindingEntry:
    explainable_presentation_binding_id: str
    presentation_route_id: str
    command_intent: str
    view_id: str
    panel_id: str
    display_id: str
    display_role: str
    selected_zone_id: str
    resolution_source: str
    explainable_binding_id: str
    explainable_binding_status: str
    presentation_route_bound: bool
    explainable_source_bound: bool
    explanation_text_available: bool
    explanation_payload_available: bool
    multilingual_ready: bool
    read_only: bool
    action_execution_allowed: bool
    direct_display_switching_allowed: bool
    binding_ready: bool
    description: str

    def __post_init__(self) -> None:
        binding_id = _ensure_non_empty_str(
            self.explainable_presentation_binding_id,
            "explainable_presentation_binding_id",
        )
        if not _BINDING_ID_PATTERN.fullmatch(binding_id):
            raise ValueError(f"Invalid explainable_presentation_binding_id: {binding_id}")

        for field_name in (
            "presentation_route_id",
            "command_intent",
            "view_id",
            "panel_id",
            "display_id",
            "display_role",
            "selected_zone_id",
            "resolution_source",
            "explainable_binding_id",
            "explainable_binding_status",
            "description",
        ):
            _ensure_non_empty_str(getattr(self, field_name), field_name)

        for field_name in (
            "presentation_route_bound",
            "explainable_source_bound",
            "explanation_text_available",
            "explanation_payload_available",
            "multilingual_ready",
            "read_only",
            "action_execution_allowed",
            "direct_display_switching_allowed",
            "binding_ready",
        ):
            _ensure_bool(getattr(self, field_name), field_name)

        if not self.presentation_route_bound:
            raise ValueError("presentation_route_bound must be True")
        if not self.explainable_source_bound:
            raise ValueError("explainable_source_bound must be True")
        if not self.explanation_text_available:
            raise ValueError("explanation_text_available must be True")
        if not self.explanation_payload_available:
            raise ValueError("explanation_payload_available must be True")
        if not self.multilingual_ready:
            raise ValueError("multilingual_ready must be True")
        if not self.read_only:
            raise ValueError("read_only must be True")
        if self.action_execution_allowed:
            raise ValueError("action_execution_allowed must be False")
        if self.direct_display_switching_allowed:
            raise ValueError("direct_display_switching_allowed must be False")
        if not self.binding_ready:
            raise ValueError("binding_ready must be True")


@dataclass(frozen=True, slots=True)
class ExplainablePresentationBindingContract:
    total_bindings: int
    ready_bindings: int
    presentation_route_bound_bindings: int
    explainable_source_bound_bindings: int
    explanation_text_bindings: int
    explanation_payload_bindings: int
    multilingual_ready_bindings: int
    read_only_bindings: int
    action_execution_allowed_bindings: int
    direct_display_switching_allowed_bindings: int
    dashboard_bound_bindings: int
    route_bound_bindings: int
    entries: tuple[ExplainablePresentationBindingEntry, ...]

    def __post_init__(self) -> None:
        if self.total_bindings != len(self.entries):
            raise ValueError("total_bindings must match entries length")
        if self.total_bindings <= 0:
            raise ValueError("total_bindings must be >= 1")

        expected = {
            "ready_bindings": sum(1 for entry in self.entries if entry.binding_ready),
            "presentation_route_bound_bindings": sum(
                1 for entry in self.entries if entry.presentation_route_bound
            ),
            "explainable_source_bound_bindings": sum(
                1 for entry in self.entries if entry.explainable_source_bound
            ),
            "explanation_text_bindings": sum(
                1 for entry in self.entries if entry.explanation_text_available
            ),
            "explanation_payload_bindings": sum(
                1 for entry in self.entries if entry.explanation_payload_available
            ),
            "multilingual_ready_bindings": sum(
                1 for entry in self.entries if entry.multilingual_ready
            ),
            "read_only_bindings": sum(1 for entry in self.entries if entry.read_only),
            "action_execution_allowed_bindings": sum(
                1 for entry in self.entries if entry.action_execution_allowed
            ),
            "direct_display_switching_allowed_bindings": sum(
                1 for entry in self.entries if entry.direct_display_switching_allowed
            ),
            "dashboard_bound_bindings": sum(
                1 for entry in self.entries if entry.resolution_source == "dashboard_read_only_view"
            ),
            "route_bound_bindings": sum(
                1 for entry in self.entries if entry.resolution_source == "display_orchestration_route"
            ),
        }

        for field_name, expected_value in expected.items():
            if getattr(self, field_name) != expected_value:
                raise ValueError(f"{field_name} must match computed count")

        if self.ready_bindings != self.total_bindings:
            raise ValueError("all explainable presentation bindings must be ready")
        if self.presentation_route_bound_bindings != self.total_bindings:
            raise ValueError("all bindings must be presentation-route-bound")
        if self.explainable_source_bound_bindings != self.total_bindings:
            raise ValueError("all bindings must be explainable-source-bound")
        if self.explanation_text_bindings != self.total_bindings:
            raise ValueError("all bindings must have explanation text")
        if self.explanation_payload_bindings != self.total_bindings:
            raise ValueError("all bindings must have explanation payload")
        if self.multilingual_ready_bindings != self.total_bindings:
            raise ValueError("all bindings must be multilingual-ready")
        if self.read_only_bindings != self.total_bindings:
            raise ValueError("all bindings must be read-only")
        if self.action_execution_allowed_bindings != 0:
            raise ValueError("explainable presentation bindings must not execute actions")
        if self.direct_display_switching_allowed_bindings != 0:
            raise ValueError("explainable presentation bindings must not switch displays")
        if self.dashboard_bound_bindings <= 0:
            raise ValueError("at least one explainable binding must be dashboard-bound")
        if self.route_bound_bindings <= 0:
            raise ValueError("at least one explainable binding must be route-bound")


def build_explainable_presentation_binding_contract() -> ExplainablePresentationBindingContract:
    router = build_presentation_router_contract()
    explainable = build_explainable_view_binding_contract()

    entries: list[ExplainablePresentationBindingEntry] = []

    for route in router.entries:
        matched = _match_explainable_entry(route, explainable.entries)
        binding_id = route.presentation_route_id.replace(
            "presentation_route_",
            "explainable_presentation_binding_",
            1,
        )

        entries.append(
            ExplainablePresentationBindingEntry(
                explainable_presentation_binding_id=binding_id,
                presentation_route_id=route.presentation_route_id,
                command_intent=route.command_intent,
                view_id=route.resolved_view_id,
                panel_id=route.resolved_panel_id,
                display_id=route.selected_display_id,
                display_role=route.selected_display_role,
                selected_zone_id=route.selected_zone_id,
                resolution_source=route.resolution_source,
                explainable_binding_id=matched.binding_id,
                explainable_binding_status=str(matched.binding_status),
                presentation_route_bound=route.presentation_ready,
                explainable_source_bound=True,
                explanation_text_available=matched.explanation_text_available,
                explanation_payload_available=matched.explanation_payload_available,
                multilingual_ready=matched.multilingual_ready,
                read_only=route.read_only,
                action_execution_allowed=route.action_execution_allowed,
                direct_display_switching_allowed=route.direct_display_switching_allowed,
                binding_ready=(
                    route.presentation_ready
                    and matched.explanation_text_available
                    and matched.explanation_payload_available
                    and matched.multilingual_ready
                    and route.read_only
                    and not route.action_execution_allowed
                    and not route.direct_display_switching_allowed
                ),
                description=f"Read-only explainable presentation binding for {route.command_intent}.",
            )
        )

    contract_entries = tuple(entries)

    return ExplainablePresentationBindingContract(
        total_bindings=len(contract_entries),
        ready_bindings=sum(1 for entry in contract_entries if entry.binding_ready),
        presentation_route_bound_bindings=sum(
            1 for entry in contract_entries if entry.presentation_route_bound
        ),
        explainable_source_bound_bindings=sum(
            1 for entry in contract_entries if entry.explainable_source_bound
        ),
        explanation_text_bindings=sum(
            1 for entry in contract_entries if entry.explanation_text_available
        ),
        explanation_payload_bindings=sum(
            1 for entry in contract_entries if entry.explanation_payload_available
        ),
        multilingual_ready_bindings=sum(
            1 for entry in contract_entries if entry.multilingual_ready
        ),
        read_only_bindings=sum(1 for entry in contract_entries if entry.read_only),
        action_execution_allowed_bindings=sum(
            1 for entry in contract_entries if entry.action_execution_allowed
        ),
        direct_display_switching_allowed_bindings=sum(
            1 for entry in contract_entries if entry.direct_display_switching_allowed
        ),
        dashboard_bound_bindings=sum(
            1 for entry in contract_entries if entry.resolution_source == "dashboard_read_only_view"
        ),
        route_bound_bindings=sum(
            1 for entry in contract_entries if entry.resolution_source == "display_orchestration_route"
        ),
        entries=contract_entries,
    )

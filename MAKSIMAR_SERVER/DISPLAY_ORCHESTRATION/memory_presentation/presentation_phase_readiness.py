from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Dict, Tuple

from MAKSIMAR_SERVER.DISPLAY_ORCHESTRATION.memory_presentation.presentation_preview_builder import (
    build_presentation_preview,
)
from MAKSIMAR_SERVER.DISPLAY_ORCHESTRATION.memory_presentation.presentation_router import (
    build_presentation_router_contract,
)
from MAKSIMAR_SERVER.DISPLAY_ORCHESTRATION.memory_presentation.presentation_summary_builder import (
    build_presentation_summary,
)


_FORBIDDEN_PRESENTATION_ROOTS = (
    "dashboard_root",
    "display_manager_root",
    "gesture_root",
    "navigation_root",
    "explainability_root",
)


@dataclass(frozen=True, slots=True)
class PresentationPhaseReadiness:
    presentation_requests: int
    view_resolutions: int
    panel_resolutions: int
    display_target_selections: int
    presentation_routes: int
    dashboard_bound_routes: int
    route_bound_routes: int
    flow: Tuple[str, ...]
    requests_ready: bool
    views_ready: bool
    panels_ready: bool
    targets_ready: bool
    router_ready: bool
    source_bound_ready: bool
    registry_routed_ready: bool
    multi_display_selection_ready: bool
    action_execution_allowed: int
    direct_display_switching_allowed: int
    no_new_presentation_roots: bool
    phase_ready: bool


def _no_forbidden_presentation_roots() -> bool:
    return not any(Path(root_name).exists() for root_name in _FORBIDDEN_PRESENTATION_ROOTS)


def build_presentation_phase_readiness() -> PresentationPhaseReadiness:
    summary = build_presentation_summary()
    preview = build_presentation_preview()
    router = build_presentation_router_contract()

    requests_ready = (
        int(summary["presentation_ready_requests"])
        == int(summary["presentation_requests"])
    )
    views_ready = (
        int(summary["view_ready_resolutions"])
        == int(summary["view_resolutions"])
        and int(summary["view_source_bound_resolutions"])
        == int(summary["view_resolutions"])
    )
    panels_ready = (
        int(summary["panel_ready_resolutions"])
        == int(summary["panel_resolutions"])
        and int(summary["panel_source_bound_resolutions"])
        == int(summary["panel_resolutions"])
    )
    targets_ready = (
        int(summary["display_target_ready_selections"])
        == int(summary["display_target_selections"])
    )
    router_ready = (
        int(summary["presentation_ready_routes"])
        == int(summary["presentation_routes"])
        and int(summary["presentation_registry_routed_routes"])
        == int(summary["presentation_routes"])
    )
    source_bound_ready = (
        int(summary["presentation_source_bound_routes"])
        == int(summary["presentation_routes"])
    )
    registry_routed_ready = (
        int(summary["presentation_registry_routed_routes"])
        == int(summary["presentation_routes"])
    )
    selected_display_ids = tuple(entry.selected_display_id for entry in router.entries)
    multi_display_selection_ready = len(set(selected_display_ids)) == len(selected_display_ids)

    action_execution_allowed = (
        int(summary["presentation_action_execution_allowed_requests"])
        + int(summary["panel_action_execution_allowed"])
        + int(summary["presentation_action_execution_allowed_routes"])
    )
    direct_display_switching_allowed = (
        int(summary["presentation_direct_display_switching_allowed_requests"])
        + int(summary["display_target_direct_switching_allowed"])
        + int(summary["presentation_direct_display_switching_allowed_routes"])
    )
    no_new_presentation_roots = _no_forbidden_presentation_roots()

    phase_ready = (
        bool(summary["summary_ready"])
        and bool(preview["preview_ready"])
        and requests_ready
        and views_ready
        and panels_ready
        and targets_ready
        and router_ready
        and source_bound_ready
        and registry_routed_ready
        and multi_display_selection_ready
        and action_execution_allowed == 0
        and direct_display_switching_allowed == 0
        and no_new_presentation_roots
    )

    return PresentationPhaseReadiness(
        presentation_requests=int(summary["presentation_requests"]),
        view_resolutions=int(summary["view_resolutions"]),
        panel_resolutions=int(summary["panel_resolutions"]),
        display_target_selections=int(summary["display_target_selections"]),
        presentation_routes=int(summary["presentation_routes"]),
        dashboard_bound_routes=int(summary["presentation_dashboard_bound_routes"]),
        route_bound_routes=int(summary["presentation_route_bound_routes"]),
        flow=tuple(str(item) for item in preview["flow"]),
        requests_ready=requests_ready,
        views_ready=views_ready,
        panels_ready=panels_ready,
        targets_ready=targets_ready,
        router_ready=router_ready,
        source_bound_ready=source_bound_ready,
        registry_routed_ready=registry_routed_ready,
        multi_display_selection_ready=multi_display_selection_ready,
        action_execution_allowed=action_execution_allowed,
        direct_display_switching_allowed=direct_display_switching_allowed,
        no_new_presentation_roots=no_new_presentation_roots,
        phase_ready=phase_ready,
    )


def build_presentation_phase_preview() -> Dict[str, object]:
    readiness = build_presentation_phase_readiness()

    return {
        "flow": readiness.flow,
        "preview_ready": readiness.phase_ready,
        "phase_ready": readiness.phase_ready,
        "presentation_requests": readiness.presentation_requests,
        "view_resolutions": readiness.view_resolutions,
        "panel_resolutions": readiness.panel_resolutions,
        "display_target_selections": readiness.display_target_selections,
        "presentation_routes": readiness.presentation_routes,
        "dashboard_bound_routes": readiness.dashboard_bound_routes,
        "route_bound_routes": readiness.route_bound_routes,
        "requests_ready": readiness.requests_ready,
        "views_ready": readiness.views_ready,
        "panels_ready": readiness.panels_ready,
        "targets_ready": readiness.targets_ready,
        "router_ready": readiness.router_ready,
        "source_bound_ready": readiness.source_bound_ready,
        "registry_routed_ready": readiness.registry_routed_ready,
        "multi_display_selection_ready": readiness.multi_display_selection_ready,
        "action_execution_allowed": readiness.action_execution_allowed,
        "direct_display_switching_allowed": readiness.direct_display_switching_allowed,
        "no_new_presentation_roots": readiness.no_new_presentation_roots,
    }

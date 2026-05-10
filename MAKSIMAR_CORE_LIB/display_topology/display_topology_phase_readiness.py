from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Dict, Tuple

from MAKSIMAR_CORE_LIB.display_topology.display_topology_preview_builder import (
    build_display_topology_preview,
)
from MAKSIMAR_CORE_LIB.display_topology.display_topology_summary_builder import (
    build_display_topology_summary,
)


_FORBIDDEN_DISPLAY_ROOTS = (
    "dashboard_root",
    "display_manager_root",
    "gesture_root",
    "navigation_root",
    "explainability_root",
)


@dataclass(frozen=True, slots=True)
class DisplayTopologyPhaseReadiness:
    display_topology_displays: int
    display_orchestration_entries: int
    dashboard_root_entries: int
    display_registry_entries: int
    display_role_bindings: int
    zone_layout_entries: int
    display_capability_entries: int
    display_assignment_bindings: int
    flow: Tuple[str, ...]
    topology_contract_ready: bool
    display_registry_ready: bool
    display_roles_ready: bool
    zone_layout_ready: bool
    display_capabilities_ready: bool
    display_assignments_ready: bool
    orchestration_bound: bool
    dashboard_bound: bool
    skill_domain_bound: bool
    memory_views_display_bindable: bool
    multilingual_ready: bool
    explainable_ready: bool
    registry_routing_ready: bool
    action_execution_allowed: int
    backend_execution_allowed: int
    direct_switching_allowed: int
    no_new_display_roots: bool
    phase_ready: bool


def _no_forbidden_display_roots() -> bool:
    return not any(Path(root_name).exists() for root_name in _FORBIDDEN_DISPLAY_ROOTS)


def build_display_topology_phase_readiness() -> DisplayTopologyPhaseReadiness:
    summary = build_display_topology_summary()
    preview = build_display_topology_preview()

    topology_contract_ready = (
        int(summary["display_topology_displays"]) >= 3
        and summary["summary_ready"] is True
    )
    display_registry_ready = (
        int(summary["display_registry_entries"]) == int(summary["display_registry_ready_entries"])
        and int(summary["display_registry_entries"]) == int(summary["display_topology_displays"])
    )
    display_roles_ready = (
        int(summary["display_role_bindings"]) == int(summary["display_role_ready_bindings"])
        and int(summary["display_role_bindings"]) == int(summary["display_topology_displays"])
    )
    zone_layout_ready = (
        int(summary["zone_layout_entries"]) == int(summary["zone_layout_ready_entries"])
        and int(summary["zone_layout_entries"]) >= int(summary["display_topology_displays"])
    )
    display_capabilities_ready = (
        int(summary["display_capability_entries"]) == int(summary["display_capability_ready_entries"])
        and int(summary["display_capability_entries"]) >= int(summary["display_topology_displays"])
    )
    display_assignments_ready = (
        int(summary["display_assignment_bindings"]) == int(summary["display_assignment_ready_bindings"])
        and int(summary["display_assignment_bindings"]) == int(summary["display_orchestration_entries"])
    )
    orchestration_bound = (
        int(summary["display_orchestration_entries"]) >= 3
        and int(summary["display_orchestration_registry_routed_entries"])
        == int(summary["display_orchestration_entries"])
    )
    dashboard_bound = (
        bool(summary["dashboard_read_only_phase_ready"])
        and int(summary["dashboard_active_entries"])
        == int(summary["dashboard_root_entries"])
    )
    skill_domain_bound = (
        bool(summary["skill_domain_summary_ready"])
        and bool(summary["skill_domain_preview_ready"])
    )
    memory_views_display_bindable = bool(summary["memory_views_display_bindable"])
    multilingual_ready = (
        int(summary["display_topology_multilingual_ready_displays"])
        == int(summary["display_topology_displays"])
    )
    explainable_ready = (
        int(summary["display_topology_explainable_displays"])
        == int(summary["display_topology_displays"])
    )
    registry_routing_ready = (
        int(summary["display_topology_registry_routed_displays"])
        == int(summary["display_topology_displays"])
    )
    no_new_display_roots = _no_forbidden_display_roots()

    phase_ready = (
        topology_contract_ready
        and display_registry_ready
        and display_roles_ready
        and zone_layout_ready
        and display_capabilities_ready
        and display_assignments_ready
        and orchestration_bound
        and dashboard_bound
        and skill_domain_bound
        and memory_views_display_bindable
        and multilingual_ready
        and explainable_ready
        and registry_routing_ready
        and int(summary["action_execution_allowed"]) == 0
        and int(summary["backend_execution_allowed"]) == 0
        and int(summary["direct_switching_allowed"]) == 0
        and no_new_display_roots
        and bool(preview["preview_ready"])
    )

    return DisplayTopologyPhaseReadiness(
        display_topology_displays=int(summary["display_topology_displays"]),
        display_orchestration_entries=int(summary["display_orchestration_entries"]),
        dashboard_root_entries=int(summary["dashboard_root_entries"]),
        display_registry_entries=int(summary["display_registry_entries"]),
        display_role_bindings=int(summary["display_role_bindings"]),
        zone_layout_entries=int(summary["zone_layout_entries"]),
        display_capability_entries=int(summary["display_capability_entries"]),
        display_assignment_bindings=int(summary["display_assignment_bindings"]),
        flow=tuple(str(item) for item in preview["flow"]),
        topology_contract_ready=topology_contract_ready,
        display_registry_ready=display_registry_ready,
        display_roles_ready=display_roles_ready,
        zone_layout_ready=zone_layout_ready,
        display_capabilities_ready=display_capabilities_ready,
        display_assignments_ready=display_assignments_ready,
        orchestration_bound=orchestration_bound,
        dashboard_bound=dashboard_bound,
        skill_domain_bound=skill_domain_bound,
        memory_views_display_bindable=memory_views_display_bindable,
        multilingual_ready=multilingual_ready,
        explainable_ready=explainable_ready,
        registry_routing_ready=registry_routing_ready,
        action_execution_allowed=int(summary["action_execution_allowed"]),
        backend_execution_allowed=int(summary["backend_execution_allowed"]),
        direct_switching_allowed=int(summary["direct_switching_allowed"]),
        no_new_display_roots=no_new_display_roots,
        phase_ready=phase_ready,
    )


def build_display_topology_phase_preview() -> Dict[str, object]:
    readiness = build_display_topology_phase_readiness()

    return {
        "flow": readiness.flow,
        "preview_ready": readiness.phase_ready,
        "phase_ready": readiness.phase_ready,
        "display_topology_displays": readiness.display_topology_displays,
        "display_orchestration_entries": readiness.display_orchestration_entries,
        "dashboard_root_entries": readiness.dashboard_root_entries,
        "display_registry_entries": readiness.display_registry_entries,
        "display_role_bindings": readiness.display_role_bindings,
        "zone_layout_entries": readiness.zone_layout_entries,
        "display_capability_entries": readiness.display_capability_entries,
        "display_assignment_bindings": readiness.display_assignment_bindings,
        "topology_contract_ready": readiness.topology_contract_ready,
        "display_registry_ready": readiness.display_registry_ready,
        "display_roles_ready": readiness.display_roles_ready,
        "zone_layout_ready": readiness.zone_layout_ready,
        "display_capabilities_ready": readiness.display_capabilities_ready,
        "display_assignments_ready": readiness.display_assignments_ready,
        "orchestration_bound": readiness.orchestration_bound,
        "dashboard_bound": readiness.dashboard_bound,
        "skill_domain_bound": readiness.skill_domain_bound,
        "memory_views_display_bindable": readiness.memory_views_display_bindable,
        "multilingual_ready": readiness.multilingual_ready,
        "explainable_ready": readiness.explainable_ready,
        "registry_routing_ready": readiness.registry_routing_ready,
        "action_execution_allowed": readiness.action_execution_allowed,
        "backend_execution_allowed": readiness.backend_execution_allowed,
        "direct_switching_allowed": readiness.direct_switching_allowed,
        "no_new_display_roots": readiness.no_new_display_roots,
    }

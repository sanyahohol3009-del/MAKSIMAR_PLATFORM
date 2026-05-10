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
    flow: Tuple[str, ...]
    topology_contract_ready: bool
    orchestration_bound: bool
    dashboard_bound: bool
    skill_domain_bound: bool
    multilingual_ready: bool
    explainable_ready: bool
    registry_routing_ready: bool
    action_execution_allowed: int
    backend_execution_allowed: int
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
        and orchestration_bound
        and dashboard_bound
        and skill_domain_bound
        and multilingual_ready
        and explainable_ready
        and registry_routing_ready
        and int(summary["action_execution_allowed"]) == 0
        and int(summary["backend_execution_allowed"]) == 0
        and no_new_display_roots
        and bool(preview["preview_ready"])
    )

    return DisplayTopologyPhaseReadiness(
        display_topology_displays=int(summary["display_topology_displays"]),
        display_orchestration_entries=int(summary["display_orchestration_entries"]),
        dashboard_root_entries=int(summary["dashboard_root_entries"]),
        flow=tuple(str(item) for item in preview["flow"]),
        topology_contract_ready=topology_contract_ready,
        orchestration_bound=orchestration_bound,
        dashboard_bound=dashboard_bound,
        skill_domain_bound=skill_domain_bound,
        multilingual_ready=multilingual_ready,
        explainable_ready=explainable_ready,
        registry_routing_ready=registry_routing_ready,
        action_execution_allowed=int(summary["action_execution_allowed"]),
        backend_execution_allowed=int(summary["backend_execution_allowed"]),
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
        "topology_contract_ready": readiness.topology_contract_ready,
        "orchestration_bound": readiness.orchestration_bound,
        "dashboard_bound": readiness.dashboard_bound,
        "skill_domain_bound": readiness.skill_domain_bound,
        "multilingual_ready": readiness.multilingual_ready,
        "explainable_ready": readiness.explainable_ready,
        "registry_routing_ready": readiness.registry_routing_ready,
        "action_execution_allowed": readiness.action_execution_allowed,
        "backend_execution_allowed": readiness.backend_execution_allowed,
        "no_new_display_roots": readiness.no_new_display_roots,
    }

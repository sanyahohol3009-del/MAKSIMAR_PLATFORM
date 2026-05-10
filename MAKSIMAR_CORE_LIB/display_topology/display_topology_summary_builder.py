from __future__ import annotations

from typing import Dict

from MAKSIMAR_CORE_LIB.display_topology.display_topology_contract import (
    build_display_topology_contract,
)
from MAKSIMAR_CORE_LIB.skill_domain_binding import build_skill_domain_preview
from MAKSIMAR_SERVER.DASHBOARD_READ_ONLY_VIEWS import (
    build_dashboard_read_only_views_contract,
    build_dashboard_read_only_views_phase_readiness,
)
from MAKSIMAR_SERVER.DISPLAY_ORCHESTRATION import (
    build_display_orchestration_contract,
)


def build_display_topology_summary() -> Dict[str, object]:
    topology = build_display_topology_contract()
    orchestration = build_display_orchestration_contract()
    dashboard = build_dashboard_read_only_views_contract()
    dashboard_readiness = build_dashboard_read_only_views_phase_readiness()
    skill_domain = build_skill_domain_preview()

    explainable_displays = sum(
        1 for entry in topology.entries if entry.supports_explainable_views
    )
    registry_routed_displays = sum(
        1 for entry in topology.entries if entry.supports_registry_routing
    )
    active_displays = sum(
        1 for entry in topology.entries if entry.availability_status == "active"
    )

    action_execution_allowed = (
        int(skill_domain["shell_action_execution_allowed_bindings"])
        + int(skill_domain["skill_to_dashboard_action_execution_allowed_bindings"])
    )

    backend_execution_allowed = int(
        skill_domain["skill_to_retrieval_backend_execution_allowed_bindings"]
    )

    summary_ready = (
        topology.total_displays == len(topology.entries)
        and topology.total_displays >= 3
        and topology.multilingual_ready_displays == topology.total_displays
        and explainable_displays == topology.total_displays
        and registry_routed_displays == topology.total_displays
        and active_displays == topology.total_displays
        and orchestration.total_entries >= 3
        and orchestration.explanation_required_entries == orchestration.total_entries
        and orchestration.registry_routed_entries == orchestration.total_entries
        and orchestration.multilingual_ready_entries == orchestration.total_entries
        and dashboard_readiness.phase_ready is True
        and dashboard.active_entries == dashboard.total_entries
        and bool(skill_domain["summary_ready"])
        and bool(skill_domain["preview_ready"])
        and action_execution_allowed == 0
        and backend_execution_allowed == 0
    )

    return {
        "display_topology_displays": topology.total_displays,
        "display_topology_private_displays": topology.private_displays,
        "display_topology_shared_displays": topology.shared_displays,
        "display_topology_multilingual_ready_displays": topology.multilingual_ready_displays,
        "display_topology_explainable_displays": explainable_displays,
        "display_topology_registry_routed_displays": registry_routed_displays,
        "display_topology_active_displays": active_displays,
        "display_orchestration_entries": orchestration.total_entries,
        "display_orchestration_explanation_required_entries": orchestration.explanation_required_entries,
        "display_orchestration_registry_routed_entries": orchestration.registry_routed_entries,
        "display_orchestration_multilingual_ready_entries": orchestration.multilingual_ready_entries,
        "dashboard_root_entries": dashboard.total_entries,
        "dashboard_active_entries": dashboard.active_entries,
        "dashboard_read_only_phase_ready": dashboard_readiness.phase_ready,
        "skill_domain_summary_ready": skill_domain["summary_ready"],
        "skill_domain_preview_ready": skill_domain["preview_ready"],
        "action_execution_allowed": action_execution_allowed,
        "backend_execution_allowed": backend_execution_allowed,
        "summary_ready": summary_ready,
    }

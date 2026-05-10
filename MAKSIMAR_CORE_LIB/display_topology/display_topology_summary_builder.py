from __future__ import annotations

from typing import Dict

from MAKSIMAR_CORE_LIB.display_topology.display_assignment_binding_models import (
    build_display_assignment_binding_contract,
)
from MAKSIMAR_CORE_LIB.display_topology.display_capability_models import (
    build_display_capability_binding_contract,
)
from MAKSIMAR_CORE_LIB.display_topology.display_registry_models import (
    build_display_registry_contract,
)
from MAKSIMAR_CORE_LIB.display_topology.display_role_models import (
    build_display_role_binding_contract,
)
from MAKSIMAR_CORE_LIB.display_topology.display_topology_contract import (
    build_display_topology_contract,
)
from MAKSIMAR_CORE_LIB.display_topology.zone_layout_models import (
    build_zone_layout_contract,
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
    display_registry = build_display_registry_contract()
    display_roles = build_display_role_binding_contract()
    zone_layout = build_zone_layout_contract()
    capabilities = build_display_capability_binding_contract()
    assignments = build_display_assignment_binding_contract()

    topology_display_ids = {entry.display_id for entry in topology.entries}
    dashboard_display_ids = {entry.display_id for entry in dashboard.entries}
    memory_views_display_bindable = dashboard_display_ids.issubset(topology_display_ids)

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

    direct_switching_allowed = (
        display_registry.direct_switching_allowed_entries
        + capabilities.direct_execution_allowed_capabilities
        + assignments.direct_switching_allowed_assignments
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
        and display_registry.ready_entries == display_registry.total_entries
        and display_roles.ready_roles == display_roles.total_roles
        and zone_layout.ready_zones == zone_layout.total_zones
        and capabilities.ready_capabilities == capabilities.total_capabilities
        and assignments.ready_assignments == assignments.total_assignments
        and memory_views_display_bindable
        and action_execution_allowed == 0
        and backend_execution_allowed == 0
        and direct_switching_allowed == 0
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
        "display_registry_entries": display_registry.total_entries,
        "display_registry_ready_entries": display_registry.ready_entries,
        "display_role_bindings": display_roles.total_roles,
        "display_role_ready_bindings": display_roles.ready_roles,
        "zone_layout_entries": zone_layout.total_zones,
        "zone_layout_ready_entries": zone_layout.ready_zones,
        "display_capability_entries": capabilities.total_capabilities,
        "display_capability_ready_entries": capabilities.ready_capabilities,
        "display_assignment_bindings": assignments.total_assignments,
        "display_assignment_ready_bindings": assignments.ready_assignments,
        "memory_views_display_bindable": memory_views_display_bindable,
        "action_execution_allowed": action_execution_allowed,
        "backend_execution_allowed": backend_execution_allowed,
        "direct_switching_allowed": direct_switching_allowed,
        "summary_ready": summary_ready,
    }

from __future__ import annotations

from MAKSIMAR_CORE_LIB.display_topology import (
    build_display_topology_contract,
)
from MAKSIMAR_SERVER.MEMORY_REGISTRY import (
    build_memory_registry_contract,
)
from MAKSIMAR_SERVER.REGISTRY_AUTO_ENROLLMENT import (
    build_registry_auto_enrollment_contract,
)
from MAKSIMAR_SERVER.SKILL_ADAPTER_REGISTRY import (
    build_skill_adapter_registry_contract,
)
from MAKSIMAR_SERVER.DISPLAY_ORCHESTRATION.display_orchestration_models import (
    DisplayOrchestrationContract,
    DisplayOrchestrationEntry,
)


def build_display_orchestration_contract() -> DisplayOrchestrationContract:
    """Build canonical presentation/display orchestration contract."""
    display_topology = build_display_topology_contract()
    memory_registry = build_memory_registry_contract()
    skill_registry = build_skill_adapter_registry_contract()
    auto_enrollment = build_registry_auto_enrollment_contract()

    display_by_role = {
        entry.display_role: entry for entry in display_topology.entries
    }

    memory_panel_id = memory_registry.entries[0].panel_ids[0]
    simulation_panel_id = skill_registry.entries[0].panel_ids[0]

    monitoring_entries = [
        entry
        for entry in auto_enrollment.entries
        if entry.module_slug == "monitoring_panel"
    ]
    if len(monitoring_entries) != 1:
        raise ValueError("Expected exactly one monitoring panel registry entry")

    monitoring_panel_id = monitoring_entries[0].panel_ids[0]

    mobile_display = display_by_role["mobile_display_proxy"]
    engineering_display = display_by_role["engineering_display"]
    primary_display = display_by_role["primary_dashboard_display"]

    entries = (
        DisplayOrchestrationEntry(
            route_request_id="displayroute_show_memory_001",
            command_intent="show_memory",
            resolved_view_id="view_memory_project_architecture",
            selected_display_id=mobile_display.display_id,
            selected_display_role=mobile_display.display_role,
            selected_zone_id=mobile_display.zone_ids[0],
            selected_panel_id=memory_panel_id,
            explanation_required=True,
            registry_routed=True,
            multilingual_ready=mobile_display.supports_multilingual_rendering,
            route_status="routed",
            description=(
                "Display orchestration for memory presentation routed to the private mobile display proxy."
            ),
        ),
        DisplayOrchestrationEntry(
            route_request_id="displayroute_show_simulation_001",
            command_intent="show_simulation",
            resolved_view_id="view_simulation_skill_overview",
            selected_display_id=engineering_display.display_id,
            selected_display_role=engineering_display.display_role,
            selected_zone_id=engineering_display.zone_ids[0],
            selected_panel_id=simulation_panel_id,
            explanation_required=True,
            registry_routed=True,
            multilingual_ready=engineering_display.supports_multilingual_rendering,
            route_status="routed",
            description=(
                "Display orchestration for simulation presentation routed to the engineering display."
            ),
        ),
        DisplayOrchestrationEntry(
            route_request_id="displayroute_show_monitoring_001",
            command_intent="show_monitoring",
            resolved_view_id="view_monitoring_panel",
            selected_display_id=primary_display.display_id,
            selected_display_role=primary_display.display_role,
            selected_zone_id=primary_display.zone_ids[0],
            selected_panel_id=monitoring_panel_id,
            explanation_required=True,
            registry_routed=True,
            multilingual_ready=primary_display.supports_multilingual_rendering,
            route_status="routed",
            description=(
                "Display orchestration for monitoring presentation routed to the primary dashboard display."
            ),
        ),
    )

    explanation_required_entries = sum(
        1 for entry in entries if entry.explanation_required
    )
    registry_routed_entries = sum(
        1 for entry in entries if entry.registry_routed
    )
    multilingual_ready_entries = sum(
        1 for entry in entries if entry.multilingual_ready
    )

    return DisplayOrchestrationContract(
        total_entries=len(entries),
        explanation_required_entries=explanation_required_entries,
        registry_routed_entries=registry_routed_entries,
        multilingual_ready_entries=multilingual_ready_entries,
        entries=entries,
    )

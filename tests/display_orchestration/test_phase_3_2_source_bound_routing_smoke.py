from __future__ import annotations

from MAKSIMAR_SERVER.DISPLAY_ORCHESTRATION.memory_presentation import (
    build_presentation_router_contract,
)


def test_phase_3_2_source_bound_routing_smoke() -> None:
    router = build_presentation_router_contract()

    assert router.source_bound_routes == router.total_routes
    assert router.dashboard_bound_routes == 2
    assert router.route_bound_routes == 1

    monitoring = next(
        entry for entry in router.entries if entry.command_intent == "show_monitoring"
    )

    assert monitoring.resolution_source == "display_orchestration_route"
    assert monitoring.resolved_view_id == "view_monitoring_panel"
    assert monitoring.resolved_panel_id == "panel_monitoring_panel"
    assert monitoring.selected_display_id == "display_primary_dashboard_001"
    assert monitoring.selected_zone_id == "zone_dashboard_main"

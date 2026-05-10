from __future__ import annotations

from MAKSIMAR_SERVER.DISPLAY_ORCHESTRATION.memory_presentation import (
    build_presentation_router_contract,
)


def test_registered_memory_view_presentable_smoke() -> None:
    contract = build_presentation_router_contract()

    memory_route = next(
        entry for entry in contract.entries if entry.command_intent == "show_memory"
    )

    assert memory_route.resolved_view_id == "view_memory_project_architecture"
    assert memory_route.resolved_panel_id == "panel_memory_project_architecture"
    assert memory_route.selected_display_id == "display_mobile_proxy_001"
    assert memory_route.selected_zone_id == "zone_mobile_main"
    assert memory_route.resolution_source == "dashboard_read_only_view"
    assert memory_route.presentation_ready is True

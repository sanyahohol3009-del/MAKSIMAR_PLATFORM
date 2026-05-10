from __future__ import annotations

from MAKSIMAR_SERVER.DISPLAY_ORCHESTRATION.memory_presentation import (
    build_presentation_router_contract,
)


def test_presentation_router_smoke() -> None:
    contract = build_presentation_router_contract()

    assert contract.total_routes == 3
    assert contract.ready_routes == contract.total_routes
    assert contract.request_bound_routes == contract.total_routes
    assert contract.view_bound_routes == contract.total_routes
    assert contract.panel_bound_routes == contract.total_routes
    assert contract.target_bound_routes == contract.total_routes
    assert contract.source_bound_routes == contract.total_routes
    assert contract.registry_routed_routes == contract.total_routes
    assert contract.read_only_routes == contract.total_routes
    assert contract.action_execution_allowed_routes == 0
    assert contract.direct_display_switching_allowed_routes == 0
    assert contract.dashboard_bound_routes == 2
    assert contract.route_bound_routes == 1

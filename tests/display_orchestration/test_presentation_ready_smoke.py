from __future__ import annotations

from MAKSIMAR_SERVER.DISPLAY_ORCHESTRATION.memory_presentation import (
    build_presentation_preview,
    build_presentation_router_contract,
    build_presentation_summary,
)


def test_presentation_ready_smoke() -> None:
    router = build_presentation_router_contract()
    summary = build_presentation_summary()
    preview = build_presentation_preview()

    assert router.ready_routes == router.total_routes
    assert router.source_bound_routes == router.total_routes
    assert router.registry_routed_routes == router.total_routes
    assert router.action_execution_allowed_routes == 0
    assert router.direct_display_switching_allowed_routes == 0

    assert summary["summary_ready"] is True
    assert summary["presentation_routes"] == 3
    assert summary["presentation_ready_routes"] == 3
    assert summary["presentation_dashboard_bound_routes"] == 2
    assert summary["presentation_route_bound_routes"] == 1

    assert preview["preview_ready"] is True
    assert preview["presentation_routes"] == 3
    assert preview["presentation_ready_routes"] == 3
    assert preview["action_execution_allowed"] == 0
    assert preview["direct_display_switching_allowed"] == 0

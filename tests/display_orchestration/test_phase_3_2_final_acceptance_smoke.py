from __future__ import annotations

from MAKSIMAR_SERVER.DISPLAY_ORCHESTRATION.memory_presentation import (
    build_presentation_phase_preview,
    build_presentation_phase_readiness,
    build_presentation_preview,
    build_presentation_router_contract,
    build_presentation_summary,
)


def test_phase_3_2_final_acceptance_smoke() -> None:
    router = build_presentation_router_contract()
    summary = build_presentation_summary()
    preview = build_presentation_preview()
    readiness = build_presentation_phase_readiness()
    phase_preview = build_presentation_phase_preview()

    assert router.total_routes == 3
    assert router.ready_routes == router.total_routes
    assert router.dashboard_bound_routes == 2
    assert router.route_bound_routes == 1
    assert router.source_bound_routes == router.total_routes
    assert router.registry_routed_routes == router.total_routes
    assert router.action_execution_allowed_routes == 0
    assert router.direct_display_switching_allowed_routes == 0

    assert summary["summary_ready"] is True
    assert preview["preview_ready"] is True
    assert readiness.phase_ready is True
    assert phase_preview["phase_ready"] is True
    assert phase_preview["preview_ready"] is True

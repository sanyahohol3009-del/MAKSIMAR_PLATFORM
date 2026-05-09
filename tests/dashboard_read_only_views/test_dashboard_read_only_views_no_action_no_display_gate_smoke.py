from __future__ import annotations

from MAKSIMAR_SERVER.DASHBOARD_READ_ONLY_VIEWS import (
    build_dashboard_read_only_views_phase_readiness,
)


def test_dashboard_read_only_views_no_action_no_display_gate_smoke() -> None:
    readiness = build_dashboard_read_only_views_phase_readiness()

    assert readiness.no_action_exposure is True
    assert readiness.no_display_orchestration is True
    assert readiness.no_mutation_surface is True

from __future__ import annotations

from MAKSIMAR_SERVER.DASHBOARD_READ_ONLY_VIEWS import (
    build_dashboard_read_only_views_phase_readiness,
)


def test_dashboard_read_only_views_phase_readiness_gate_smoke() -> None:
    readiness = build_dashboard_read_only_views_phase_readiness()

    assert readiness.phase_ready is True
    assert readiness.root_contract_ready is True
    assert readiness.memory_registry_views_bound is True
    assert readiness.read_only_enforced is True

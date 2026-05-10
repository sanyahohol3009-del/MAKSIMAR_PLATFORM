from __future__ import annotations

from MAKSIMAR_CORE_LIB.display_topology import (
    build_display_topology_phase_preview,
    build_display_topology_phase_readiness,
)


def test_display_topology_phase_readiness_smoke() -> None:
    readiness = build_display_topology_phase_readiness()
    preview = build_display_topology_phase_preview()

    assert readiness.phase_ready is True
    assert readiness.topology_contract_ready is True
    assert readiness.orchestration_bound is True
    assert readiness.dashboard_bound is True
    assert readiness.skill_domain_bound is True
    assert readiness.multilingual_ready is True
    assert readiness.explainable_ready is True
    assert readiness.registry_routing_ready is True
    assert readiness.action_execution_allowed == 0
    assert readiness.backend_execution_allowed == 0
    assert readiness.no_new_display_roots is True

    assert preview["preview_ready"] is True
    assert preview["phase_ready"] is True

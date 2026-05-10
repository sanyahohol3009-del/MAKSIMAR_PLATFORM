from __future__ import annotations

from MAKSIMAR_CORE_LIB.display_topology import (
    build_display_topology_contract,
    build_display_topology_phase_readiness,
    build_display_topology_preview,
    build_display_topology_summary,
)


def test_phase_3_1_batch1_ready_smoke() -> None:
    contract = build_display_topology_contract()
    summary = build_display_topology_summary()
    preview = build_display_topology_preview()
    readiness = build_display_topology_phase_readiness()

    assert contract.total_displays == 3
    assert summary["summary_ready"] is True
    assert preview["preview_ready"] is True
    assert readiness.phase_ready is True
    assert readiness.action_execution_allowed == 0
    assert readiness.backend_execution_allowed == 0

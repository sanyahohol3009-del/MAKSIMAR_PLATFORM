from __future__ import annotations

from MAKSIMAR_SERVER.EXECUTION_CONTROL.artifact_routing import (
    build_storage_artifact_phase_readiness,
)


def test_storage_artifact_readiness_gate_smoke() -> None:
    readiness = build_storage_artifact_phase_readiness()

    assert readiness.phase_ready is True
    assert readiness.storage_core_ready is True
    assert readiness.artifact_binding_ready is True
    assert readiness.data_plane_route_ready is True
    assert readiness.dashboard_preview_ready is True

from __future__ import annotations

from MAKSIMAR_SERVER.EXECUTION_CONTROL.artifact_routing import (
    build_media_memory_artifact_phase_readiness,
)


def test_media_memory_artifact_readiness_gate_smoke() -> None:
    readiness = build_media_memory_artifact_phase_readiness()

    assert readiness.phase_ready is True
    assert readiness.media_core_ready is True
    assert readiness.artifact_routing_ready is True
    assert readiness.data_plane_route_reference_ready is True
    assert readiness.dashboard_preview_ready is True

from __future__ import annotations

from MAKSIMAR_CORE_LIB.memory_engine.media_memory import (
    build_media_memory_phase_readiness,
)
from MAKSIMAR_SERVER.EXECUTION_CONTROL.artifact_routing import (
    build_media_memory_artifact_phase_readiness,
)


def test_media_memory_phase_1_6_ready_smoke() -> None:
    core_readiness = build_media_memory_phase_readiness()
    server_readiness = build_media_memory_artifact_phase_readiness()

    assert core_readiness.phase_core_ready is True
    assert server_readiness.phase_ready is True
    assert server_readiness.media_core_records == core_readiness.total_records

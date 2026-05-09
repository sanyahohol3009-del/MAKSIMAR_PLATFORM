from __future__ import annotations

from MAKSIMAR_CORE_LIB.memory_engine.storage_registry import (
    build_storage_registry_phase_readiness,
)
from MAKSIMAR_SERVER.EXECUTION_CONTROL.artifact_routing import (
    build_storage_artifact_phase_readiness,
)


def test_storage_phase_1_5_ready_smoke() -> None:
    core_readiness = build_storage_registry_phase_readiness()
    server_readiness = build_storage_artifact_phase_readiness()

    assert core_readiness.phase_core_ready is True
    assert server_readiness.phase_ready is True
    assert server_readiness.storage_core_entries == core_readiness.total_entries

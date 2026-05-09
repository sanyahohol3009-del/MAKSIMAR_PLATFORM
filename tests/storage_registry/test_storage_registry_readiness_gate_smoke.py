from __future__ import annotations

from MAKSIMAR_CORE_LIB.memory_engine.storage_registry import (
    build_storage_registry_phase_readiness,
)


def test_storage_registry_readiness_gate_smoke() -> None:
    readiness = build_storage_registry_phase_readiness()

    assert readiness.phase_core_ready is True
    assert readiness.preview_ready is True
    assert readiness.flow_ready is True
    assert readiness.m2_nas_ready is True

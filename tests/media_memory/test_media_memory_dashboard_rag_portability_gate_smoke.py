from __future__ import annotations

from MAKSIMAR_CORE_LIB.memory_engine.media_memory import (
    build_media_memory_phase_readiness,
)


def test_media_memory_dashboard_rag_portability_gate_smoke() -> None:
    readiness = build_media_memory_phase_readiness()

    assert readiness.dashboard_visible_records == readiness.total_records
    assert readiness.retrieval_visible_records >= 1
    assert readiness.storage_bindings == readiness.total_records
    assert readiness.storage_ready_bindings == readiness.storage_bindings
    assert readiness.binary_external_bindings == readiness.storage_bindings
    assert readiness.dashboard_rag_ready is True

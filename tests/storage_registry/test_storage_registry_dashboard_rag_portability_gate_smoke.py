from __future__ import annotations

from MAKSIMAR_CORE_LIB.memory_engine.storage_registry import (
    build_storage_registry_phase_readiness,
)


def test_storage_registry_dashboard_rag_portability_gate_smoke() -> None:
    readiness = build_storage_registry_phase_readiness()

    assert readiness.dashboard_visible_entries == readiness.total_entries
    assert readiness.retrieval_visible_entries >= 1
    assert readiness.relocation_ready_entries == readiness.total_entries
    assert readiness.nas_ready_entries == readiness.total_entries
    assert readiness.retrieval_index_ready is True

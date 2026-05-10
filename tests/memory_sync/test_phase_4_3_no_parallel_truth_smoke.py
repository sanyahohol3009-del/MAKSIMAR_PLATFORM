from __future__ import annotations

from MAKSIMAR_SERVER.MEMORY_SYNC import (
    build_memory_sync_phase_readiness,
    build_memory_sync_summary,
)


def test_phase_4_3_no_parallel_truth_smoke() -> None:
    summary = build_memory_sync_summary()
    readiness = build_memory_sync_phase_readiness()

    assert summary["canonical_write_allowed"] == 0
    assert summary["client_canonical_write_allowed"] == 0
    assert summary["parallel_truth_allowed"] == 0
    assert summary["runtime_mutation_allowed"] == 0
    assert summary["auto_conflict_resolution_allowed"] == 0
    assert readiness.no_canonical_write is True
    assert readiness.no_client_canonical_write is True
    assert readiness.no_parallel_truth is True
    assert readiness.no_runtime_mutation is True
    assert readiness.no_auto_conflict_resolution is True

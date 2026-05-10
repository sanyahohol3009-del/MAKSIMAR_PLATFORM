from __future__ import annotations

from MAKSIMAR_SERVER.MEMORY_SYNC import (
    build_memory_sync_conflict_guard_contract,
    build_memory_sync_preview,
    build_memory_sync_route_contract,
    build_memory_sync_summary,
)


def test_phase_4_3_batch2_ready_smoke() -> None:
    routes = build_memory_sync_route_contract()
    guards = build_memory_sync_conflict_guard_contract()
    summary = build_memory_sync_summary()
    preview = build_memory_sync_preview()

    assert routes.ready_routes == routes.total_routes
    assert guards.ready_guards == guards.total_guards
    assert summary["summary_ready"] is True
    assert preview["preview_ready"] is True
    assert summary["canonical_write_allowed"] == 0
    assert summary["parallel_truth_allowed"] == 0
    assert summary["auto_conflict_resolution_allowed"] == 0

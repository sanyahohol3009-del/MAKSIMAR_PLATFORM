from __future__ import annotations

from MAKSIMAR_SERVER.MEMORY_SYNC import (
    build_memory_sync_phase_preview,
    build_memory_sync_phase_readiness,
    build_memory_sync_preview,
    build_memory_sync_summary,
)


def test_phase_4_3_final_acceptance_smoke() -> None:
    summary = build_memory_sync_summary()
    preview = build_memory_sync_preview()
    readiness = build_memory_sync_phase_readiness()
    phase_preview = build_memory_sync_phase_preview()

    assert summary["summary_ready"] is True
    assert preview["preview_ready"] is True
    assert readiness.phase_ready is True
    assert phase_preview["phase_ready"] is True
    assert phase_preview["preview_ready"] is True

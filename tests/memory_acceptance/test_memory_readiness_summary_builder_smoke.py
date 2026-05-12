from __future__ import annotations

from MAKSIMAR_SERVER.MEMORY_ACCEPTANCE import build_memory_readiness_summary


def test_memory_readiness_summary_builder_smoke() -> None:
    summary = build_memory_readiness_summary()

    assert summary["readiness_ready"] is True
    assert summary["roadmap_family"] == "memory_roadmap_v5_1"
    assert summary["phase_id"] == "PHASE 6.0"
    assert summary["track_scope"] == "memory"
    assert summary["failed_gates"] == 0
    assert summary["write_policy_ready"] is True

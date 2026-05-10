from __future__ import annotations

from MAKSIMAR_SERVER.CONTROL_PLANE.memory_routing.adapters import build_mempalace_summary


def test_mempalace_summary_builder_smoke() -> None:
    summary = build_mempalace_summary()

    assert summary["summary_ready"] is True
    assert summary["adapters"] == 1
    assert summary["capabilities"] == 4
    assert summary["queries"] == 4
    assert summary["write_requests"] == 4
    assert summary["source_of_truth_adapters"] == 0
    assert summary["canonical_write_allowed"] == 0
    assert summary["auto_promotion_allowed"] == 0
    assert summary["auto_conflict_resolution_allowed"] == 0
    assert summary["runtime_mutation_allowed"] == 0

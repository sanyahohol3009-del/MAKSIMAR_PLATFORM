from __future__ import annotations

from MAKSIMAR_SERVER.OBSERVABILITY.memory_skill_metrics.final_roadmap_closure_summary_builder import (
    build_final_roadmap_closure_summary,
)


def test_final_roadmap_closure_summary_builder_smoke() -> None:
    summary = build_final_roadmap_closure_summary()

    assert summary["summary_ready"] is True
    assert summary["roadmap_family"] == "memory_roadmap_v5_1"
    assert summary["closed_phase"] == "PHASE 6.8"
    assert summary["recommended_next_entrypoint"] == "multi_tenant_multi_country_regulatory_memory_track"
    assert summary["final_closure_ready"] is True

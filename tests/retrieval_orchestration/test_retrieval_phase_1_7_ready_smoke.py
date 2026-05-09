from __future__ import annotations

from MAKSIMAR_SERVER.CONTROL_PLANE.memory_routing import (
    build_retrieval_batch2_preview,
    build_retrieval_phase_readiness,
    build_retrieval_preview,
)


def test_retrieval_phase_1_7_ready_smoke() -> None:
    preview = build_retrieval_preview()
    batch2 = build_retrieval_batch2_preview()
    readiness = build_retrieval_phase_readiness()

    assert preview["preview_ready"] is True
    assert preview["route_ready"] is True
    assert batch2["batch2_ready"] is True
    assert readiness.phase_ready is True
    assert readiness.selected_source_count == preview["selected_source_count"]
    assert readiness.evidence_item_count == preview["evidence_item_count"]

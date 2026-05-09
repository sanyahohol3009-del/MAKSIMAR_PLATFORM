from __future__ import annotations

from MAKSIMAR_SERVER.CONTROL_PLANE.memory_routing import (
    build_evidence_source_chain_preview,
)


def test_evidence_source_chain_preview_smoke() -> None:
    preview = build_evidence_source_chain_preview()

    assert preview["preview_ready"] is True
    assert preview["phase_batch_ready"] is True
    assert preview["flow"] == (
        "retrieval_evidence_pack",
        "source_binding",
        "provenance_binding",
        "trace_binding",
        "citation_gate",
        "conflict_gate",
        "dashboard_read_only_visibility",
        "evidence_source_chain_ready",
    )

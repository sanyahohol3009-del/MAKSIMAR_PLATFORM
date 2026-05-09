from __future__ import annotations

from MAKSIMAR_SERVER.CONTROL_PLANE.memory_routing import (
    build_evidence_bound_memory_phase_preview,
)


def test_evidence_bound_memory_phase_preview_smoke() -> None:
    preview = build_evidence_bound_memory_phase_preview()

    assert preview["preview_ready"] is True
    assert preview["phase_ready"] is True
    assert preview["flow"] == (
        "retrieval_phase_readiness",
        "evidence_source_chain",
        "source_bound_gate",
        "provenance_bound_gate",
        "trace_bound_gate",
        "citation_required_gate",
        "conflict_clear_gate",
        "backend_policy_gate",
        "evidence_bound_memory_readiness",
    )

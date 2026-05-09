from __future__ import annotations

from MAKSIMAR_SERVER.CONTROL_PLANE.memory_routing import (
    build_evidence_memory_core_binding_preview,
)


def test_evidence_memory_core_binding_preview_smoke() -> None:
    preview = build_evidence_memory_core_binding_preview()

    assert preview["preview_ready"] is True
    assert preview["phase_batch_ready"] is True
    assert preview["flow"] == (
        "core_evidence_memory",
        "server_evidence_source_chain",
        "evidence_id_match",
        "artifact_ref_match",
        "citation_gate",
        "conflict_clear_gate",
        "memory_truth_gate",
        "knowledge_graph_projection_gate",
        "read_only_gate",
        "backend_policy_gate",
        "core_server_binding_ready",
    )

from __future__ import annotations

from MAKSIMAR_CORE_LIB.memory_policy import build_governance_preview


def test_governance_preview_builder_smoke() -> None:
    preview = build_governance_preview()

    assert preview["preview_ready"] is True
    assert preview["phase_batch_ready"] is True
    assert preview["flow"] == (
        "memory_classification_policy",
        "memory_policy_scope",
        "core_evidence_memory",
        "governance_binding",
        "approval_required_gate",
        "conflict_resolution_gate",
        "controlled_promotion_gate",
        "knowledge_graph_projection_gate",
        "read_only_gate",
        "governance_preview",
    )

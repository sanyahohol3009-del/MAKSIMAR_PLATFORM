from __future__ import annotations

from MAKSIMAR_CORE_LIB.evidence_memory import build_evidence_memory_preview


def test_evidence_memory_preview_builder_smoke() -> None:
    preview = build_evidence_memory_preview()

    assert preview["preview_ready"] is True
    assert preview["phase_batch_ready"] is True
    assert preview["flow"] == (
        "source_event",
        "source_version_chain",
        "conflict_marker",
        "evidence_memory_record",
        "citation_required_gate",
        "knowledge_graph_projection_gate",
        "read_only_gate",
        "evidence_memory_ready",
    )

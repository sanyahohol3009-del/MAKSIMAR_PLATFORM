from __future__ import annotations

from pathlib import Path

from MAKSIMAR_SERVER.REGULATORY_MEMORY_FOUNDATION import build_regulatory_memory_final_closure_preview


def test_regulatory_memory_final_closure_acceptance_smoke() -> None:
    regulatory_doc = Path("docs/architecture/roadmap_index/regulatory_memory_final_closure_v1.md")
    complete_doc = Path("docs/architecture/roadmap_index/memory_foundation_complete_final_closure_v1.md")
    preview = build_regulatory_memory_final_closure_preview()

    assert regulatory_doc.exists()
    assert complete_doc.exists()
    assert preview["preview_ready"] is True
    assert preview["closed_step_count"] == 9
    assert preview["acceptance_doc_count"] == 10
    assert preview["leak_detected"] is False
    assert preview["cross_tenant_retrieval_allowed"] is False
    assert preview["cross_tenant_merge_allowed"] is False
    assert preview["cross_jurisdiction_merge_allowed"] is False
    assert preview["auto_routing_merge_allowed"] is False

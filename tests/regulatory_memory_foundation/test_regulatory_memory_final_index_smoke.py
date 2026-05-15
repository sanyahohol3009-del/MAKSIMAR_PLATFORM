from __future__ import annotations

from MAKSIMAR_SERVER.REGULATORY_MEMORY_FOUNDATION import build_regulatory_memory_final_index_preview


def test_regulatory_memory_final_index_smoke() -> None:
    preview = build_regulatory_memory_final_index_preview()

    assert preview["preview_ready"] is True
    assert preview["closed_step_count"] == 9
    assert preview["acceptance_doc_count"] == 10
    assert preview["missing_acceptance_docs"] == ()
    assert preview["routing_preview_ready"] is True
    assert preview["runtime_mutation_allowed"] is False
    assert preview["direct_core_write_allowed"] is False

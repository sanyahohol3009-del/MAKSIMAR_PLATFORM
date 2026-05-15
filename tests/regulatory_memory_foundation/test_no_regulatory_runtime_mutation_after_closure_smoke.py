from __future__ import annotations

from MAKSIMAR_SERVER.REGULATORY_MEMORY_FOUNDATION import build_regulatory_memory_final_closure_preview


def test_no_regulatory_runtime_mutation_after_closure_smoke() -> None:
    preview = build_regulatory_memory_final_closure_preview()

    assert preview["runtime_mutation_allowed"] is False
    assert preview["direct_core_write_allowed"] is False
    assert preview["canonical_truth_update_allowed"] is False
    assert preview["auto_apply_allowed"] is False
    assert preview["deployment_allowed_now"] is False
    assert preview["external_release_allowed_now"] is False

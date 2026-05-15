from __future__ import annotations

from MAKSIMAR_SERVER.REGULATORY_MEMORY_FOUNDATION import build_regulatory_update_diff_preview


def test_regulatory_update_diff_builder_smoke() -> None:
    preview = build_regulatory_update_diff_preview()

    assert preview["preview_ready"] is True
    assert preview["diff_entry_count"] >= 2
    assert preview["approval_gate_ready"] is True
    assert preview["approval_required"] is True
    assert preview["approval_granted"] is False
    assert preview["auto_apply_allowed"] is False
    assert preview["canonical_truth_update_allowed"] is False
    assert preview["runtime_mutation_allowed"] is False

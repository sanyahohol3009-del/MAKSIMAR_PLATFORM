from __future__ import annotations

from pathlib import Path

from MAKSIMAR_SERVER.REGULATORY_MEMORY_FOUNDATION import build_regulatory_update_approval_preview


def test_regulatory_update_approval_acceptance_smoke() -> None:
    doc = Path("docs/architecture/foundation/regulatory_update_approval_gate_v1.md")
    preview = build_regulatory_update_approval_preview()

    assert doc.exists()
    assert preview["preview_ready"] is True
    assert preview["current_step"] == "STEP 7 — Regulatory Update Approval Gate"
    assert preview["next_step"] == "STEP 8 — Regulatory Routing / No Cross-Tenant Leak"
    assert preview["proposal_count"] >= 2
    assert preview["diff_entry_count"] >= 2
    assert preview["approval_gate_required"] is True
    assert preview["approval_required"] is True
    assert preview["approval_granted"] is False
    assert preview["proposal_only"] is True
    assert preview["diff_required"] is True
    assert preview["operator_review_required"] is True
    assert preview["auto_apply_allowed"] is False
    assert preview["canonical_truth_update_allowed"] is False
    assert preview["runtime_mutation_allowed"] is False
    assert preview["direct_core_write_allowed"] is False
    assert preview["deployment_allowed_now"] is False

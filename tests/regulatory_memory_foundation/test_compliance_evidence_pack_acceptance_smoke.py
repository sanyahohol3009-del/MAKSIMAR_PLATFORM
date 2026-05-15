from __future__ import annotations

from pathlib import Path

from MAKSIMAR_SERVER.REGULATORY_MEMORY_FOUNDATION import build_compliance_evidence_pack_preview


def test_compliance_evidence_pack_acceptance_smoke() -> None:
    doc = Path("docs/architecture/foundation/compliance_evidence_pack_audit_read_model_v1.md")
    preview = build_compliance_evidence_pack_preview()

    assert doc.exists()
    assert preview["preview_ready"] is True
    assert preview["current_step"] == "STEP 6 — Compliance Evidence Pack / Audit Read Model"
    assert preview["next_step"] == "STEP 7 — Regulatory Update Approval Gate"
    assert preview["evidence_item_count"] >= 3
    assert preview["audit_entry_count"] >= 3
    assert preview["source_to_decision_trace_required"] is True
    assert preview["source_to_decision_trace_ready"] is True
    assert preview["audit_read_model_ready"] is True
    assert preview["operator_visible"] is True
    assert preview["read_only"] is True
    assert preview["automatic_resolution_allowed"] is False
    assert preview["canonical_truth_update_allowed"] is False
    assert preview["runtime_mutation_allowed"] is False
    assert preview["direct_core_write_allowed"] is False
    assert preview["deployment_allowed_now"] is False

from __future__ import annotations

from MAKSIMAR_SERVER.REGULATORY_MEMORY_FOUNDATION import build_compliance_evidence_pack


def test_compliance_evidence_pack_models_smoke() -> None:
    pack = build_compliance_evidence_pack()

    assert pack.evidence_pack_ready is True
    assert len(pack.evidence_items) >= 3
    assert pack.source_registry_ready is True
    assert pack.conflict_drift_supersession_ready is True
    assert pack.source_to_decision_trace_required is True
    assert pack.audit_read_model_required is True
    assert pack.human_review_required is True
    assert pack.automatic_resolution_allowed is False
    assert pack.canonical_truth_update_allowed is False

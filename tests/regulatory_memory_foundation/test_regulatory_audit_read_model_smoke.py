from __future__ import annotations

from MAKSIMAR_SERVER.REGULATORY_MEMORY_FOUNDATION import build_regulatory_audit_read_model_preview


def test_regulatory_audit_read_model_smoke() -> None:
    preview = build_regulatory_audit_read_model_preview()

    assert preview["preview_ready"] is True
    assert preview["audit_entry_count"] >= 3
    assert preview["evidence_pack_ready"] is True
    assert preview["conflict_drift_supersession_ready"] is True
    assert preview["operator_visible"] is True
    assert preview["read_only"] is True
    assert preview["mutation_allowed"] is False
    assert preview["automatic_resolution_allowed"] is False

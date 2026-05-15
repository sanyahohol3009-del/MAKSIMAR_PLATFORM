from __future__ import annotations

from MAKSIMAR_SERVER.REGULATORY_MEMORY_FOUNDATION import build_compliance_traceability_preview


def test_compliance_traceability_builder_smoke() -> None:
    preview = build_compliance_traceability_preview()

    assert preview["preview_ready"] is True
    assert preview["trace_step_count"] >= 8
    assert "source_ref" in preview["trace_steps"]
    assert "source_version" in preview["trace_steps"]
    assert "effective_date" in preview["trace_steps"]
    assert "audit_read_model" in preview["trace_steps"]
    assert preview["source_to_decision_trace_ready"] is True
    assert preview["operator_visible"] is True
    assert preview["mutation_allowed"] is False

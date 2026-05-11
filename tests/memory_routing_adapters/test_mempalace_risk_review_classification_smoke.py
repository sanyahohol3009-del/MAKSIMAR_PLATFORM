from __future__ import annotations

from MAKSIMAR_SERVER.CONTROL_PLANE.memory_routing.adapters import (
    build_mempalace_risk_review_classification_report,
)


def test_mempalace_risk_review_classification_smoke() -> None:
    report = build_mempalace_risk_review_classification_report()

    assert report.classification_ready is True
    assert report.total_findings == report.classified_findings
    assert report.total_findings > 0
    assert report.production_surface_findings > 0
    assert report.forbidden_until_review_findings > 0
    assert report.hard_gate_passed is True
    assert report.manual_security_review_required is True
    assert report.manual_security_review_completed is False
    assert report.real_backend_enablement_allowed is False
    assert report.real_backend_query_allowed is False
    assert report.canonical_write_allowed is False
    assert report.runtime_mutation_allowed is False

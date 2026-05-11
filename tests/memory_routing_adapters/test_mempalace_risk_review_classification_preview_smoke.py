from __future__ import annotations

from MAKSIMAR_SERVER.CONTROL_PLANE.memory_routing.adapters import (
    build_mempalace_risk_review_classification_preview,
)


def test_mempalace_risk_review_classification_preview_smoke() -> None:
    preview = build_mempalace_risk_review_classification_preview()

    assert preview["classification_ready"] is True
    assert preview["total_findings"] == preview["classified_findings"]
    assert preview["manual_security_review_required"] is True
    assert preview["manual_security_review_completed"] is False
    assert preview["real_backend_enablement_allowed"] is False
    assert preview["real_backend_query_allowed"] is False
    assert preview["canonical_write_allowed"] is False
    assert preview["runtime_mutation_allowed"] is False

from __future__ import annotations

from MAKSIMAR_SERVER.CONTROL_PLANE.memory_routing.adapters import (
    build_mempalace_risk_review_classification_preview,
)


def test_phase_5_1_batch4b_ready_smoke() -> None:
    preview = build_mempalace_risk_review_classification_preview()

    assert preview["classification_ready"] is True
    assert preview["forbidden_until_review_findings"] > 0
    assert preview["real_backend_enablement_allowed"] is False
    assert preview["real_backend_query_allowed"] is False

from __future__ import annotations

import json

from MAKSIMAR_SERVER.CONTROL_PLANE.memory_routing.adapters import (
    write_mempalace_risk_review_classification_report,
)


def test_mempalace_risk_review_report_written_smoke() -> None:
    path = write_mempalace_risk_review_classification_report()

    assert path.exists()

    payload = json.loads(path.read_text(encoding="utf-8"))

    assert payload["classification_ready"] is True
    assert payload["total_findings"] == payload["classified_findings"]
    assert payload["manual_security_review_required"] is True
    assert payload["manual_security_review_completed"] is False
    assert payload["real_backend_enablement_allowed"] is False
    assert payload["real_backend_query_allowed"] is False

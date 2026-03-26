from __future__ import annotations

from MAKSIMAR_CORE_LIB.source_of_truth import (
    build_summary_incident_alert_consistency_check,
)


def test_summary_incident_alert_consistency_build() -> None:
    """Summary ↔ incident ↔ alert consistency should build."""
    result = build_summary_incident_alert_consistency_check()

    assert result.check_scope == "summary_incident_alert"
    assert result.total_lines >= 1
    assert isinstance(result.overall_consistent, bool)

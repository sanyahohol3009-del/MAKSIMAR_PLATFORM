from __future__ import annotations

from MAKSIMAR_CORE_LIB.source_of_truth import (
    build_snapshot_metrics_consistency_check,
    build_summary_incident_alert_consistency_check,
)

from MAKSIMAR_CORE_LIB.source_of_truth.consistency_models import (
    ConsistencyCheckResult,
)


class UnifiedConsistencyReport:
    """Aggregated consistency report across all system layers."""

    def __init__(
        self,
        checks: list[ConsistencyCheckResult],
    ) -> None:
        self.checks = checks
        self.total_checks = len(checks)
        self.total_lines = sum(c.total_lines for c in checks)
        self.overall_consistent = all(c.overall_consistent for c in checks)


def build_unified_consistency_report() -> UnifiedConsistencyReport:
    """Build unified consistency report from all checks."""

    checks: list[ConsistencyCheckResult] = [
        build_snapshot_metrics_consistency_check(),
        build_summary_incident_alert_consistency_check(),
    ]

    return UnifiedConsistencyReport(checks=checks)

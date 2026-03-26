from __future__ import annotations

from MAKSIMAR_CORE_LIB.oob_dashboard.consistency_panel_models import (
    DashboardConsistencyPanel,
)
from MAKSIMAR_CORE_LIB.source_of_truth import (
    build_unified_consistency_report,
)


def build_dashboard_consistency_panel() -> DashboardConsistencyPanel:
    """Build read-only dashboard consistency panel from unified report."""
    report = build_unified_consistency_report()

    return DashboardConsistencyPanel(
        panel_id="dashboard_consistency_panel",
        overall_consistent=report.overall_consistent,
        total_checks=report.total_checks,
        total_lines=report.total_lines,
        status="consistent" if report.overall_consistent else "inconsistent",
    )

from __future__ import annotations

from MAKSIMAR_CORE_LIB.oob_dashboard.snapshot_aggregator import (
    build_dashboard_state_snapshot,
)
from MAKSIMAR_CORE_LIB.oob_dashboard.incident_view import (
    build_dashboard_incident_view,
)

from MAKSIMAR_CORE_LIB.source_of_truth.consistency_models import (
    ConsistencyCheckLine,
    ConsistencyCheckResult,
)


def build_summary_incident_alert_consistency_check() -> ConsistencyCheckResult:
    """
    Validate consistency between:
    - summary (snapshot)
    - incident view
    - alert-level interpretation
    """

    snapshot = build_dashboard_state_snapshot()
    incident_view = build_dashboard_incident_view()

    lines: list[ConsistencyCheckLine] = []

    # 1. overall_status consistency
    lines.append(
        ConsistencyCheckLine(
            check_name="overall_status_match",
            expected_value=1 if snapshot.overall_status == incident_view.overall_status else 0,
            actual_value=1,
            consistent=snapshot.overall_status == incident_view.overall_status,
        )
    )

    # 2. total lines consistency
    lines.append(
        ConsistencyCheckLine(
            check_name="total_lines_match",
            expected_value=snapshot.total_lines,
            actual_value=incident_view.total_lines,
            consistent=snapshot.total_lines == incident_view.total_lines,
        )
    )

    # 3. problem signal alignment
    snapshot_has_problem = snapshot.overall_status != "ok"
    incident_has_problem = any(
        line.status != "ok" for line in incident_view.lines
    )

    lines.append(
        ConsistencyCheckLine(
            check_name="problem_signal_alignment",
            expected_value=1 if snapshot_has_problem else 0,
            actual_value=1 if incident_has_problem else 0,
            consistent=snapshot_has_problem == incident_has_problem,
        )
    )

    overall_consistent = all(line.consistent for line in lines)

    return ConsistencyCheckResult(
        check_scope="summary_incident_alert",
        overall_consistent=overall_consistent,
        total_lines=len(lines),
        lines=lines,
    )

from __future__ import annotations

from MAKSIMAR_CORE_LIB.oob_dashboard.snapshot_aggregator import (
    build_dashboard_state_snapshot,
)
from MAKSIMAR_CORE_LIB.source_of_truth.consistency_models import (
    ConsistencyCheckLine,
    ConsistencyCheckResult,
)


def build_snapshot_metrics_consistency_check() -> ConsistencyCheckResult:
    """
    Validate that snapshot layer and derived metrics are consistent.
    """

    snapshot = build_dashboard_state_snapshot()

    lines: list[ConsistencyCheckLine] = []

    expected_total = snapshot.total_lines
    actual_total = len(snapshot.lines)

    lines.append(
        ConsistencyCheckLine(
            check_name="snapshot_total_lines_match",
            expected_value=expected_total,
            actual_value=actual_total,
            consistent=expected_total == actual_total,
        )
    )

    consistent = all(line.consistent for line in lines)

    return ConsistencyCheckResult(
        check_scope="snapshot_metrics",
        overall_consistent=consistent,
        total_lines=len(lines),
        lines=lines,
    )

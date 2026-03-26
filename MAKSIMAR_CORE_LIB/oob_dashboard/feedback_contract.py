from __future__ import annotations

from MAKSIMAR_CORE_LIB.oob_dashboard.diagnostics_index import (
    build_diagnostics_index,
)
from MAKSIMAR_CORE_LIB.oob_dashboard.feedback_models import (
    DashboardFeedbackContract,
    DiagnosticsFeedbackItem,
)
from MAKSIMAR_CORE_LIB.oob_dashboard.snapshot_aggregator import (
    build_dashboard_state_snapshot,
)


def build_dashboard_feedback_contract() -> DashboardFeedbackContract:
    """Build unified diagnostics-to-chat feedback contract."""
    snapshot = build_dashboard_state_snapshot()
    diagnostics = build_diagnostics_index(snapshot)

    items = tuple(
        DiagnosticsFeedbackItem(
            source_name=hint.source_name,
            probable_location=hint.probable_location,
            hint_text=hint.hint_text,
        )
        for hint in diagnostics.hints
    )

    return DashboardFeedbackContract(
        total_items=len(items),
        items=items,
    )

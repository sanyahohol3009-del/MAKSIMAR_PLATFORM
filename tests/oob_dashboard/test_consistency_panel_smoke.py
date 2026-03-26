from __future__ import annotations

from MAKSIMAR_CORE_LIB.oob_dashboard import (
    build_dashboard_consistency_panel,
)


def test_dashboard_consistency_panel_builds() -> None:
    """Dashboard consistency panel should build successfully."""
    panel = build_dashboard_consistency_panel()

    assert panel.panel_id == "dashboard_consistency_panel"
    assert panel.total_checks >= 1
    assert panel.total_lines >= 1
    assert panel.status in {"consistent", "inconsistent"}


def test_dashboard_consistency_panel_is_consistent() -> None:
    """Dashboard consistency panel should reflect unified report state."""
    panel = build_dashboard_consistency_panel()

    assert panel.overall_consistent is True
    assert panel.status == "consistent"

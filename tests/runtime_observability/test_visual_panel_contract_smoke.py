from __future__ import annotations

from MAKSIMAR_CORE_LIB.runtime_observability import (
    build_runtime_observability_visual_panel,
)


def test_visual_panel_contract_builds() -> None:
    """Visual panel contract should build successfully."""
    panel = build_runtime_observability_visual_panel()

    assert panel.panel_id == "panel_runtime_observability"
    assert panel.total_metrics == 5
    assert len(panel.metrics) == 5


def test_visual_panel_contains_failed_domains() -> None:
    """Visual panel should contain failed_domains metric."""
    panel = build_runtime_observability_visual_panel()

    metric_names = {metric.metric_name for metric in panel.metrics}

    assert "failed_domains" in metric_names
    assert panel.overall_status in {"ok", "warning"}

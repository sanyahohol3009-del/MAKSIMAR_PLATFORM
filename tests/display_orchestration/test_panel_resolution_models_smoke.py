from __future__ import annotations

from MAKSIMAR_SERVER.DISPLAY_ORCHESTRATION.memory_presentation import (
    build_panel_resolution_contract,
)


def test_panel_resolution_models_smoke() -> None:
    contract = build_panel_resolution_contract()

    assert contract.total_panels == 3
    assert contract.ready_panels == contract.total_panels
    assert contract.source_bound_panels == contract.total_panels
    assert 0 <= contract.dashboard_bound_panels <= contract.total_panels
    assert contract.read_only_panels == contract.total_panels
    assert contract.action_execution_allowed_panels == 0

    monitoring = next(
        entry for entry in contract.entries if entry.resolved_panel_id == "panel_monitoring_panel"
    )
    assert monitoring.panel_dashboard_bound is False
    assert monitoring.panel_source_bound is True

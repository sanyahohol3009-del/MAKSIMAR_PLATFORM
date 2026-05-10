from __future__ import annotations

from MAKSIMAR_SERVER.DISPLAY_ORCHESTRATION.memory_presentation import (
    build_view_resolution_contract,
)


def test_view_resolution_models_smoke() -> None:
    contract = build_view_resolution_contract()

    assert contract.total_resolutions == 3
    assert contract.ready_resolutions == contract.total_resolutions
    assert contract.source_bound_resolutions == contract.total_resolutions
    assert 0 <= contract.dashboard_bound_resolutions <= contract.total_resolutions
    assert contract.explanation_available_resolutions == contract.total_resolutions
    assert contract.multilingual_ready_resolutions == contract.total_resolutions
    assert contract.read_only_resolutions == contract.total_resolutions

    monitoring = next(
        entry for entry in contract.entries if entry.command_intent == "show_monitoring"
    )
    assert monitoring.resolution_source == "display_orchestration_route"
    assert monitoring.dashboard_view_bound is False
    assert monitoring.source_bound is True
    assert monitoring.resolved_view_id == "view_monitoring_panel"
    assert monitoring.resolved_panel_id == "panel_monitoring_panel"

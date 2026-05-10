from __future__ import annotations

from MAKSIMAR_SERVER.EXPLAINABLE_VIEW_BINDING import (
    build_explainable_presentation_binding_contract,
)


def test_phase_3_3_source_bound_explanations_smoke() -> None:
    contract = build_explainable_presentation_binding_contract()

    assert contract.explainable_source_bound_bindings == contract.total_bindings
    assert contract.explanation_text_bindings == contract.total_bindings
    assert contract.explanation_payload_bindings == contract.total_bindings
    assert contract.dashboard_bound_bindings == 2
    assert contract.route_bound_bindings == 1

    monitoring = next(
        entry for entry in contract.entries if entry.command_intent == "show_monitoring"
    )

    assert monitoring.resolution_source == "display_orchestration_route"
    assert monitoring.view_id == "view_monitoring_panel"
    assert monitoring.panel_id == "panel_monitoring_panel"
    assert monitoring.explanation_text_available is True
    assert monitoring.explanation_payload_available is True
    assert monitoring.binding_ready is True

from __future__ import annotations

from MAKSIMAR_SERVER.EXPLAINABLE_VIEW_BINDING import (
    build_explainable_presentation_binding_contract,
)


def test_explainable_presentation_binding_models_smoke() -> None:
    contract = build_explainable_presentation_binding_contract()

    assert contract.total_bindings == 3
    assert contract.ready_bindings == contract.total_bindings
    assert contract.presentation_route_bound_bindings == contract.total_bindings
    assert contract.explainable_source_bound_bindings == contract.total_bindings
    assert contract.explanation_text_bindings == contract.total_bindings
    assert contract.explanation_payload_bindings == contract.total_bindings
    assert contract.multilingual_ready_bindings == contract.total_bindings
    assert contract.read_only_bindings == contract.total_bindings
    assert contract.action_execution_allowed_bindings == 0
    assert contract.direct_display_switching_allowed_bindings == 0
    assert contract.dashboard_bound_bindings == 2
    assert contract.route_bound_bindings == 1

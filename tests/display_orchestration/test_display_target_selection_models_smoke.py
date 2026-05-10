from __future__ import annotations

from MAKSIMAR_SERVER.DISPLAY_ORCHESTRATION.memory_presentation import (
    build_display_target_selection_contract,
)


def test_display_target_selection_models_smoke() -> None:
    contract = build_display_target_selection_contract()

    assert contract.total_selections == 3
    assert contract.ready_selections == contract.total_selections
    assert contract.topology_bound_selections == contract.total_selections
    assert contract.orchestration_bound_selections == contract.total_selections
    assert contract.registry_routed_selections == contract.total_selections
    assert contract.read_only_selections == contract.total_selections
    assert contract.direct_display_switching_allowed_selections == 0

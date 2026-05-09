from __future__ import annotations

from MAKSIMAR_CORE_LIB.skill_domain_binding import (
    build_domain_layer_binding_contract,
)


def test_domain_layer_binding_models_smoke() -> None:
    contract = build_domain_layer_binding_contract()

    assert contract.total_layers >= 6
    assert contract.ready_layers == contract.total_layers
    assert contract.source_exists_layers == contract.total_layers
    assert contract.registry_backed_layers == contract.total_layers
    assert contract.dashboard_visible_layers == contract.total_layers
    assert contract.read_only_layers == contract.total_layers

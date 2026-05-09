from __future__ import annotations

from MAKSIMAR_CORE_LIB.skill_domain_binding import build_skill_binding_contract


def test_skill_binding_models_smoke() -> None:
    contract = build_skill_binding_contract()

    assert contract.total_bindings >= 1
    assert contract.active_bindings == contract.total_bindings
    assert contract.ready_bindings == contract.total_bindings
    assert contract.manifest_bound_bindings == contract.total_bindings
    assert contract.registry_bound_bindings == contract.total_bindings
    assert 0 <= contract.memory_reference_bound_bindings <= contract.total_bindings
    assert contract.retrieval_reference_bound_bindings == contract.total_bindings
    assert contract.dashboard_reference_bound_bindings == contract.total_bindings

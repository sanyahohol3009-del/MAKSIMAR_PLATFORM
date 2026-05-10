from __future__ import annotations

from MAKSIMAR_SERVER.CONTROL_PLANE.memory_routing.adapters import (
    build_mempalace_adapter_contract,
)


def test_mempalace_adapter_models_smoke() -> None:
    contract = build_mempalace_adapter_contract()

    assert contract.total_adapters == 1
    assert contract.ready_adapters == contract.total_adapters
    assert contract.registry_bound_adapters == contract.total_adapters
    assert contract.policy_bound_adapters == contract.total_adapters
    assert contract.observability_bound_adapters == contract.total_adapters
    assert contract.preview_required_adapters == contract.total_adapters
    assert contract.source_of_truth_adapters == 0
    assert contract.canonical_write_allowed_adapters == 0
    assert contract.runtime_mutation_allowed_adapters == 0

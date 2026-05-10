from __future__ import annotations

from MAKSIMAR_CORE_LIB.display_topology import (
    build_display_assignment_binding_contract,
)


def test_display_assignment_binding_models_smoke() -> None:
    contract = build_display_assignment_binding_contract()

    assert contract.total_assignments == 3
    assert contract.ready_assignments == contract.total_assignments
    assert contract.topology_bound_assignments == contract.total_assignments
    assert contract.zone_bound_assignments == contract.total_assignments
    assert contract.panel_bound_assignments == contract.total_assignments
    assert contract.registry_routed_assignments == contract.total_assignments
    assert contract.read_only_assignments == contract.total_assignments
    assert contract.direct_switching_allowed_assignments == 0

from __future__ import annotations

from MAKSIMAR_CORE_LIB.skill_domain_binding import (
    build_skill_to_dashboard_binding_contract,
)


def test_skill_to_dashboard_binding_builder_smoke() -> None:
    contract = build_skill_to_dashboard_binding_contract()

    assert contract.total_bindings >= 1
    assert contract.ready_bindings == contract.total_bindings
    assert contract.dashboard_reference_bound_bindings == contract.total_bindings
    assert contract.dashboard_root_ready_bindings == contract.total_bindings
    assert contract.read_only_bindings == contract.total_bindings
    assert contract.action_execution_allowed_bindings == 0

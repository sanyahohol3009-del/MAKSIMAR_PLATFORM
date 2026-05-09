from __future__ import annotations

from MAKSIMAR_CORE_LIB.skill_domain_binding import (
    build_shell_adapter_binding_contract,
)


def test_shell_adapter_binding_models_smoke() -> None:
    contract = build_shell_adapter_binding_contract()

    assert contract.total_bindings == 4
    assert contract.ready_bindings == contract.total_bindings
    assert contract.registry_backed_bindings == contract.total_bindings
    assert contract.dashboard_visible_bindings == contract.total_bindings
    assert contract.read_only_bindings == contract.total_bindings
    assert contract.action_execution_allowed_bindings == 0

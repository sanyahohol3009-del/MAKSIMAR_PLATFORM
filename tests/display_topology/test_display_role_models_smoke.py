from __future__ import annotations

from MAKSIMAR_CORE_LIB.display_topology import build_display_role_binding_contract


def test_display_role_models_smoke() -> None:
    contract = build_display_role_binding_contract()

    assert contract.total_roles == 3
    assert contract.ready_roles == contract.total_roles
    assert contract.private_roles == 1
    assert contract.shared_roles == 2
    assert contract.operator_visible_roles == contract.total_roles
    assert contract.read_only_roles == contract.total_roles

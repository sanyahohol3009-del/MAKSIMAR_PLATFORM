from __future__ import annotations

from MAKSIMAR_CORE_LIB.skill_domain_binding import (
    build_skill_to_retrieval_binding_contract,
)


def test_skill_to_retrieval_binding_builder_smoke() -> None:
    contract = build_skill_to_retrieval_binding_contract()

    assert contract.total_bindings >= 1
    assert contract.ready_bindings == contract.total_bindings
    assert contract.retrieval_reference_bound_bindings == contract.total_bindings
    assert contract.backend_execution_allowed_bindings == 0
    assert contract.mgrep_blocked_bindings == contract.total_bindings
    assert contract.sqlite_vec_blocked_bindings == contract.total_bindings
    assert contract.read_only_bindings == contract.total_bindings

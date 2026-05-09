from __future__ import annotations

from MAKSIMAR_CORE_LIB.memory_policy import (
    build_governance_binding_contract,
    build_governance_preview,
    build_memory_policy_scope_contract,
)


def test_governance_binding_ready_smoke() -> None:
    scopes = build_memory_policy_scope_contract()
    governance = build_governance_binding_contract()
    preview = build_governance_preview()

    assert scopes.ready_scopes == scopes.total_scopes
    assert governance.ready_bindings == governance.total_bindings
    assert preview["phase_batch_ready"] is True

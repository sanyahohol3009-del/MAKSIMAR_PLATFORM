from __future__ import annotations

from MAKSIMAR_SERVER.CONTROL_PLANE.memory_routing import (
    build_evidence_source_chain_contract,
)


def test_evidence_source_chain_backend_policy_smoke() -> None:
    contract = build_evidence_source_chain_contract()

    assert contract.mgrep_blocked is True
    assert contract.sqlite_vec_blocked is True
    assert contract.backend_execution_allowed is False

from __future__ import annotations

from MAKSIMAR_CORE_LIB.evolution_debug import (
    build_sandbox_evaluation_contract,
)


def test_sandbox_evaluation_contract_builds() -> None:
    """Sandbox evaluation contract should build successfully."""
    contract = build_sandbox_evaluation_contract()

    assert contract.total_evaluations == 2
    assert len(contract.evaluations) == 2
    assert contract.deploy_allowed is False


def test_sandbox_evaluation_contract_is_core_safe() -> None:
    """Sandbox evaluations should not allow core write."""
    contract = build_sandbox_evaluation_contract()

    assert contract.evaluations[0].sandbox_executed is True
    assert contract.evaluations[0].core_write_allowed is False
    assert contract.evaluations[-1].sandbox_executed is True
    assert contract.evaluations[-1].core_write_allowed is False

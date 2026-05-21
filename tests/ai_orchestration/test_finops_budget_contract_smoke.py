from __future__ import annotations

import pytest

from MAKSIMAR_CORE_LIB.ai_orchestration.finops_budget_contract import (
    FinOpsBudgetContract,
    build_default_finops_budget_contract,
)


def test_default_finops_budget_contract_blocks_spend_and_mutation() -> None:
    contract = build_default_finops_budget_contract()

    assert contract.budget_id == "finops_budget_guard_v1"
    assert contract.budget_guard_required is True
    assert contract.budget_guard_ready is True
    assert contract.spend_execution_allowed is False
    assert contract.runtime_billing_mutation_allowed is False
    assert contract.runtime_mutation_allowed is False
    assert contract.dashboard_safe is True
    assert contract.read_only is True


def test_finops_budget_contract_rejects_spend_execution() -> None:
    with pytest.raises(ValueError, match="spend_execution_allowed"):
        FinOpsBudgetContract(
            budget_id="bad",
            budget_scope="ai_orchestration",
            hard_budget_limit_ref="ref",
            budget_guard_required=True,
            budget_guard_ready=True,
            spend_execution_allowed=True,
            runtime_billing_mutation_allowed=False,
            runtime_mutation_allowed=False,
            dashboard_safe=True,
            read_only=True,
            reason_codes=("bad",),
        )


def test_finops_budget_contract_rejects_runtime_billing_mutation() -> None:
    with pytest.raises(ValueError, match="runtime_billing_mutation_allowed"):
        FinOpsBudgetContract(
            budget_id="bad",
            budget_scope="ai_orchestration",
            hard_budget_limit_ref="ref",
            budget_guard_required=True,
            budget_guard_ready=True,
            spend_execution_allowed=False,
            runtime_billing_mutation_allowed=True,
            runtime_mutation_allowed=False,
            dashboard_safe=True,
            read_only=True,
            reason_codes=("bad",),
        )

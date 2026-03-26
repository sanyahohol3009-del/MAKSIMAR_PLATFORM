from __future__ import annotations

from MAKSIMAR_CORE_LIB.mobile_bridge import (
    build_task_result_contract,
)


def test_task_result_contract_builds() -> None:
    """Task result contract should build successfully."""
    contract = build_task_result_contract()

    assert contract.total_results == 2
    assert len(contract.results) == 2


def test_task_result_contract_is_core_safe() -> None:
    """Task results should not imply core write."""
    contract = build_task_result_contract()

    assert contract.results[0].core_write_performed is False
    assert contract.results[-1].core_write_performed is False
    assert contract.results[0].status == "completed"

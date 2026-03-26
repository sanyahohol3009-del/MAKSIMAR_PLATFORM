from __future__ import annotations

from MAKSIMAR_CORE_LIB.execution_control.admission_contract import (
    build_admission_contract,
)


def test_admission_contract_builds() -> None:
    contract = build_admission_contract()

    assert contract.total_decisions == 2
    assert len(contract.decisions) == 2


def test_admission_contract_contains_denied_request() -> None:
    contract = build_admission_contract()

    assert any(not decision.admitted for decision in contract.decisions)

from __future__ import annotations

from MAKSIMAR_CORE_LIB.execution_observability import (
    build_execution_trace_contract,
)


def test_execution_trace_contract_builds() -> None:
    contract = build_execution_trace_contract()

    assert contract.total_traces == 2
    assert len(contract.traces) == 2


def test_execution_trace_contract_has_ids() -> None:
    contract = build_execution_trace_contract()

    assert contract.traces[0].trace_id != ""
    assert contract.traces[-1].trace_id != ""

from __future__ import annotations

from MAKSIMAR_CORE_LIB.runtime_observability import (
    build_structured_logging_contract,
)


def test_logging_contract_builds() -> None:
    """Structured logging contract should build successfully."""
    contract = build_structured_logging_contract()

    assert contract.total_records == 3
    assert len(contract.records) == 3


def test_logging_contract_has_trace_ids() -> None:
    """Structured logging contract should contain trace ids."""
    contract = build_structured_logging_contract()

    assert contract.records[0].trace_id != ""
    assert contract.records[-1].trace_id != ""

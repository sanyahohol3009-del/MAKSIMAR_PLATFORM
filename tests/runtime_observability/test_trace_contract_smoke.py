from __future__ import annotations

from MAKSIMAR_CORE_LIB.runtime_observability import (
    build_trace_contract,
)


def test_trace_contract_builds() -> None:
    """Trace contract should build successfully."""
    contract = build_trace_contract()

    assert contract.total_spans == 3
    assert len(contract.spans) == 3


def test_trace_contract_has_root() -> None:
    """Trace contract should have valid root trace id."""
    contract = build_trace_contract()

    assert contract.root_trace_id != ""
    assert contract.spans[0].parent_span_id is None

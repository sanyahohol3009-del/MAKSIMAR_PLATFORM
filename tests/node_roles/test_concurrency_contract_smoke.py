from __future__ import annotations

from MAKSIMAR_CORE_LIB.node_roles import (
    build_concurrency_contract,
)


def test_concurrency_contract_builds() -> None:
    contract = build_concurrency_contract()

    assert contract.total_rules == 3
    assert len(contract.rules) == 3


def test_core_write_is_single_writer() -> None:
    contract = build_concurrency_contract()

    rule = next(r for r in contract.rules if r.resource_type == "core_write")

    assert rule.single_writer is True
    assert rule.max_parallel_tasks == 1

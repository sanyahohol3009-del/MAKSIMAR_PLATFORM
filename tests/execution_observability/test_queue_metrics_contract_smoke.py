from __future__ import annotations

from MAKSIMAR_CORE_LIB.execution_observability import (
    build_queue_metrics_contract,
)


def test_queue_metrics_contract_builds() -> None:
    """Queue metrics contract should build successfully."""
    contract = build_queue_metrics_contract()

    assert contract.total_queues == 2
    assert len(contract.queues) == 2


def test_queue_metrics_contract_contains_overloaded_queue() -> None:
    """Queue metrics contract should expose overloaded queue."""
    contract = build_queue_metrics_contract()

    assert any(queue.overloaded for queue in contract.queues)
    assert contract.queues[0].queue_name == "critical_queue"

from __future__ import annotations

from MAKSIMAR_CORE_LIB.execution_observability import (
    build_worker_saturation_metrics_contract,
)


def test_worker_saturation_metrics_contract_builds() -> None:
    """Worker saturation metrics contract should build successfully."""
    contract = build_worker_saturation_metrics_contract()

    assert contract.total_workers == 3
    assert len(contract.workers) == 3


def test_worker_saturation_metrics_contract_contains_high_saturation() -> None:
    """Worker saturation metrics contract should expose high saturation worker."""
    contract = build_worker_saturation_metrics_contract()

    assert any(worker.saturation_level == "high" for worker in contract.workers)
    assert contract.workers[0].worker_id == "worker_ai_001"

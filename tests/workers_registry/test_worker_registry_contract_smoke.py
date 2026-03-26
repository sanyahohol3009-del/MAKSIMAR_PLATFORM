from __future__ import annotations

from MAKSIMAR_CORE_LIB.workers_registry import (
    build_worker_registry_contract,
)


def test_worker_registry_contract_builds() -> None:
    """Worker registry contract should build successfully."""
    contract = build_worker_registry_contract()

    assert contract.total_workers == 3
    assert len(contract.workers) == 3


def test_worker_registry_contract_contains_expected_workers() -> None:
    """Worker registry contract should expose expected canonical workers."""
    contract = build_worker_registry_contract()

    worker_ids = {worker.worker_id for worker in contract.workers}

    assert "worker_ai_001" in worker_ids
    assert "worker_sim_001" in worker_ids
    assert "worker_voice_001" in worker_ids

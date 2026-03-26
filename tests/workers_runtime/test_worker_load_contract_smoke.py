from __future__ import annotations

from MAKSIMAR_CORE_LIB.workers_runtime import (
    build_worker_load_contract,
)


def test_worker_load_contract_builds() -> None:
    """Worker load contract should build successfully."""
    contract = build_worker_load_contract()

    assert contract.total_workers == 3
    assert len(contract.workers) == 3


def test_worker_load_contract_contains_high_saturation() -> None:
    """Worker load contract should expose high saturation worker."""
    contract = build_worker_load_contract()

    saturation_levels = {worker.saturation_level for worker in contract.workers}

    assert "high" in saturation_levels
    assert "medium" in saturation_levels

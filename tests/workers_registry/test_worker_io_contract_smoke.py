from __future__ import annotations

from MAKSIMAR_CORE_LIB.workers_registry import (
    build_worker_io_contract,
)


def test_worker_io_contract_builds() -> None:
    contract = build_worker_io_contract()

    assert contract.total_entries == 3
    assert len(contract.entries) == 3


def test_worker_io_contract_contains_simulation_worker() -> None:
    contract = build_worker_io_contract()

    worker_ids = {entry.worker_id for entry in contract.entries}

    assert "worker_sim_001" in worker_ids
    assert "worker_voice_001" in worker_ids

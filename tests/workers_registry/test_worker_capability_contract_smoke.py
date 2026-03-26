from __future__ import annotations

from MAKSIMAR_CORE_LIB.workers_registry import (
    build_worker_capability_contract,
)


def test_worker_capability_contract_builds() -> None:
    contract = build_worker_capability_contract()

    assert contract.total_capabilities == 3
    assert len(contract.capabilities) == 3


def test_worker_capability_types_present() -> None:
    contract = build_worker_capability_contract()

    types = {c.capability_type for c in contract.capabilities}

    assert "inference" in types
    assert "simulation" in types
    assert "voice_io" in types

from __future__ import annotations

from MAKSIMAR_CORE_LIB.execution_observability import (
    build_lease_metrics_contract,
)


def test_lease_metrics_contract_builds() -> None:
    """Lease metrics contract should build successfully."""
    contract = build_lease_metrics_contract()

    assert contract.total_leases == 2
    assert len(contract.leases) == 2


def test_lease_metrics_contract_contains_inactive_lease() -> None:
    """Lease metrics contract should expose inactive lease."""
    contract = build_lease_metrics_contract()

    assert any(not lease.active for lease in contract.leases)
    assert contract.leases[0].owner_worker_id == "worker_ai_001"

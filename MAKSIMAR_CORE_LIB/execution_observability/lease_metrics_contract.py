from __future__ import annotations

from MAKSIMAR_CORE_LIB.execution_control import (
    build_lease_runtime_contract,
)
from MAKSIMAR_CORE_LIB.execution_observability.lease_metrics_models import (
    LeaseMetricEntry,
    LeaseMetricsContract,
)


def build_lease_metrics_contract() -> LeaseMetricsContract:
    """Build unified deep lease metrics contract."""
    runtime = build_lease_runtime_contract()

    leases = tuple(
        LeaseMetricEntry(
            lease_id=lease.lease_id,
            owner_worker_id=lease.owner_worker_id,
            active=lease.active,
        )
        for lease in runtime.leases
    )

    return LeaseMetricsContract(
        total_leases=len(leases),
        leases=leases,
    )

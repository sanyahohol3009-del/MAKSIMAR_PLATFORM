from __future__ import annotations

from MAKSIMAR_CORE_LIB.workers_registry.worker_capability_models import (
    WorkerCapability,
    WorkerCapabilityContract,
)


def build_worker_capability_contract() -> WorkerCapabilityContract:
    """Build unified worker capability contract."""

    capabilities = (
        WorkerCapability(
            worker_id="worker_ai_001",
            capability_type="inference",
            max_concurrency=2,
            requires_gpu=True,
        ),
        WorkerCapability(
            worker_id="worker_sim_001",
            capability_type="simulation",
            max_concurrency=1,
            requires_gpu=True,
        ),
        WorkerCapability(
            worker_id="worker_voice_001",
            capability_type="voice_io",
            max_concurrency=4,
            requires_gpu=False,
        ),
    )

    return WorkerCapabilityContract(
        total_capabilities=len(capabilities),
        capabilities=capabilities,
    )

from __future__ import annotations

from MAKSIMAR_CORE_LIB.workers_registry import (
    CanonicalWorkerIdentity,
    CanonicalWorkerIdentityContract,
)


def test_worker_identity_models_build() -> None:
    """Canonical worker identity models should build successfully."""
    contract = CanonicalWorkerIdentityContract(
        total_workers=3,
        workers=(
            CanonicalWorkerIdentity(
                worker_id="worker_ai_001",
                worker_type="ai_worker",
            ),
            CanonicalWorkerIdentity(
                worker_id="worker_sim_001",
                worker_type="simulation_worker",
            ),
            CanonicalWorkerIdentity(
                worker_id="worker_voice_001",
                worker_type="voice_worker",
            ),
        ),
    )

    assert contract.total_workers == 3
    assert len(contract.workers) == 3
    assert contract.workers[0].worker_id == "worker_ai_001"
    assert contract.workers[-1].worker_type == "voice_worker"

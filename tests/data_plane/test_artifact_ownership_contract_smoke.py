from __future__ import annotations

from MAKSIMAR_CORE_LIB.data_plane import (
    build_artifact_ownership_contract,
)


def test_artifact_ownership_contract_builds() -> None:
    """Artifact ownership contract should build successfully."""
    contract = build_artifact_ownership_contract()

    assert contract.total_artifacts == 2
    assert len(contract.artifacts) == 2


def test_artifact_ownership_contract_contains_expected_workers() -> None:
    """Artifact ownership contract should expose expected owner workers."""
    contract = build_artifact_ownership_contract()

    worker_ids = {artifact.owner_worker_id for artifact in contract.artifacts}

    assert "worker_sim_001" in worker_ids
    assert "worker_ai_001" in worker_ids

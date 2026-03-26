from __future__ import annotations

from MAKSIMAR_CORE_LIB.data_plane import (
    ArtifactOwnership,
    ArtifactOwnershipContract,
)


def test_artifact_ownership_models_build() -> None:
    """Artifact ownership models should build successfully."""
    contract = ArtifactOwnershipContract(
        total_artifacts=2,
        artifacts=(
            ArtifactOwnership(
                artifact_ref="artifact://simulation/output_001",
                owner_task_id="task_env_001",
                owner_worker_id="worker_sim_001",
                retained=True,
            ),
            ArtifactOwnership(
                artifact_ref="artifact://logs/runtime_001",
                owner_task_id="task_env_002",
                owner_worker_id="worker_ai_001",
                retained=False,
            ),
        ),
    )

    assert contract.total_artifacts == 2
    assert len(contract.artifacts) == 2
    assert contract.artifacts[0].owner_worker_id == "worker_sim_001"
    assert contract.artifacts[-1].retained is False

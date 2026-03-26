from __future__ import annotations

from MAKSIMAR_CORE_LIB.data_plane.artifact_ownership_models import (
    ArtifactOwnership,
    ArtifactOwnershipContract,
)


def build_artifact_ownership_contract() -> ArtifactOwnershipContract:
    """Build unified canonical artifact ownership contract."""

    artifacts = (
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
    )

    return ArtifactOwnershipContract(
        total_artifacts=len(artifacts),
        artifacts=artifacts,
    )

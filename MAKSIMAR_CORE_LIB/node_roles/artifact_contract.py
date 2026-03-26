from __future__ import annotations

from MAKSIMAR_CORE_LIB.node_roles.artifact_models import (
    ArtifactReference,
    ArtifactReferenceContract,
)


def build_artifact_reference_contract() -> ArtifactReferenceContract:
    """Build unified artifact / data plane separation contract."""

    artifacts = (
        ArtifactReference(
            artifact_ref="artifact://simulation/output_001",
            artifact_type="simulation_dump",
            artifact_size=4096,
            owner_task_id="task_env_001",
        ),
        ArtifactReference(
            artifact_ref="artifact://media/render_001",
            artifact_type="media_render",
            artifact_size=8192,
            owner_task_id="task_env_002",
        ),
        ArtifactReference(
            artifact_ref="artifact://logs/runtime_001",
            artifact_type="runtime_log_bundle",
            artifact_size=2048,
            owner_task_id="task_env_003",
        ),
    )

    return ArtifactReferenceContract(
        total_artifacts=len(artifacts),
        artifacts=artifacts,
    )

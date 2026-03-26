from __future__ import annotations

from MAKSIMAR_CORE_LIB.data_plane.artifact_retention_models import (
    ArtifactRetentionContract,
    ArtifactRetentionRule,
)


def build_artifact_retention_contract() -> ArtifactRetentionContract:
    """Build unified artifact retention contract."""

    rules = (
        ArtifactRetentionRule(
            artifact_type="simulation_dump",
            retention_days=30,
            cleanup_allowed=True,
        ),
        ArtifactRetentionRule(
            artifact_type="media_render",
            retention_days=14,
            cleanup_allowed=True,
        ),
        ArtifactRetentionRule(
            artifact_type="runtime_log_bundle",
            retention_days=7,
            cleanup_allowed=True,
        ),
    )

    return ArtifactRetentionContract(
        total_rules=len(rules),
        rules=rules,
    )

from __future__ import annotations

from MAKSIMAR_CORE_LIB.data_plane.artifact_cleanup_models import (
    ArtifactCleanupContract,
    ArtifactCleanupRule,
)


def build_artifact_cleanup_contract() -> ArtifactCleanupContract:
    """Build unified artifact cleanup contract."""

    rules = (
        ArtifactCleanupRule(
            artifact_type="simulation_dump",
            cleanup_strategy="delete_after_retention",
            approval_required=False,
        ),
        ArtifactCleanupRule(
            artifact_type="media_render",
            cleanup_strategy="delete_after_retention",
            approval_required=False,
        ),
        ArtifactCleanupRule(
            artifact_type="runtime_log_bundle",
            cleanup_strategy="archive_then_delete",
            approval_required=True,
        ),
    )

    return ArtifactCleanupContract(
        total_rules=len(rules),
        rules=rules,
    )

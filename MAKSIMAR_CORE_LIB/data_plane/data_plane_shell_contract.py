from __future__ import annotations

from MAKSIMAR_CORE_LIB.data_plane.artifact_cleanup_contract import (
    build_artifact_cleanup_contract,
)
from MAKSIMAR_CORE_LIB.data_plane.artifact_ownership_contract import (
    build_artifact_ownership_contract,
)
from MAKSIMAR_CORE_LIB.data_plane.artifact_retention_contract import (
    build_artifact_retention_contract,
)
from MAKSIMAR_CORE_LIB.data_plane.data_plane_shell_models import (
    DataPlaneShellContract,
)


def build_data_plane_shell_contract() -> DataPlaneShellContract:
    """Build final shell contract for data plane layer."""
    ownership = build_artifact_ownership_contract()
    retention = build_artifact_retention_contract()
    cleanup = build_artifact_cleanup_contract()

    return DataPlaneShellContract(
        shell_id="data_plane_shell",
        total_ownership_entries=ownership.total_artifacts,
        total_retention_rules=retention.total_rules,
        total_cleanup_rules=cleanup.total_rules,
    )

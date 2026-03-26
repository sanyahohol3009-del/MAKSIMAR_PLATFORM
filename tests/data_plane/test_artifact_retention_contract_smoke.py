from __future__ import annotations

from MAKSIMAR_CORE_LIB.data_plane import (
    build_artifact_retention_contract,
)


def test_artifact_retention_contract_builds() -> None:
    """Artifact retention contract should build successfully."""
    contract = build_artifact_retention_contract()

    assert contract.total_rules == 3
    assert len(contract.rules) == 3


def test_artifact_retention_contract_contains_runtime_logs() -> None:
    """Artifact retention contract should contain runtime log retention rule."""
    contract = build_artifact_retention_contract()

    artifact_types = {rule.artifact_type for rule in contract.rules}

    assert "runtime_log_bundle" in artifact_types
    assert "simulation_dump" in artifact_types

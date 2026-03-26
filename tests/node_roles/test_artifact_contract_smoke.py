from __future__ import annotations

from MAKSIMAR_CORE_LIB.node_roles import (
    build_artifact_reference_contract,
)


def test_artifact_reference_contract_builds() -> None:
    """Artifact reference contract should build successfully."""
    contract = build_artifact_reference_contract()

    assert contract.total_artifacts == 3
    assert len(contract.artifacts) == 3


def test_artifact_reference_contract_contains_owner_task() -> None:
    """Artifact references should keep owner task ids."""
    contract = build_artifact_reference_contract()

    assert contract.artifacts[0].owner_task_id == "task_env_001"
    assert contract.artifacts[-1].artifact_ref.startswith("artifact://")

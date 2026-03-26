from __future__ import annotations

from MAKSIMAR_CORE_LIB.data_plane import (
    build_artifact_cleanup_contract,
)


def test_artifact_cleanup_contract_builds() -> None:
    """Artifact cleanup contract should build successfully."""
    contract = build_artifact_cleanup_contract()

    assert contract.total_rules == 3
    assert len(contract.rules) == 3


def test_artifact_cleanup_contract_contains_archive_strategy() -> None:
    """Artifact cleanup contract should contain archive strategy."""
    contract = build_artifact_cleanup_contract()

    strategies = {rule.cleanup_strategy for rule in contract.rules}

    assert "archive_then_delete" in strategies
    assert "delete_after_retention" in strategies

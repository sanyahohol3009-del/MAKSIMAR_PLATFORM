from __future__ import annotations

from MAKSIMAR_CORE_LIB.version_control import (
    build_sync_state_contract,
)


def test_sync_state_contract_builds() -> None:
    """Sync state contract should build successfully."""
    contract = build_sync_state_contract()

    assert contract.total_repos == 2
    assert len(contract.repos) == 2


def test_sync_state_contract_contains_pending_changes() -> None:
    """Sync state contract should contain pending changes state."""
    contract = build_sync_state_contract()

    states = {repo.sync_state for repo in contract.repos}

    assert "pending_changes" in states
    assert "clean" in states

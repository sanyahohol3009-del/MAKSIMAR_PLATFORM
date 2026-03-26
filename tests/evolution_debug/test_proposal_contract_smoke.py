from __future__ import annotations

from MAKSIMAR_CORE_LIB.evolution_debug import (
    build_debug_proposal_contract,
)


def test_debug_proposal_contract_builds() -> None:
    """Debug proposal contract should build successfully."""
    contract = build_debug_proposal_contract()

    assert contract.total_proposals == 1
    assert len(contract.proposals) == 1
    assert contract.deploy_allowed is False


def test_debug_proposal_requires_approval() -> None:
    """Debug proposal should remain approval-gated."""
    contract = build_debug_proposal_contract()

    assert contract.proposals[0].sandbox_verified is True
    assert contract.proposals[0].approval_required is True

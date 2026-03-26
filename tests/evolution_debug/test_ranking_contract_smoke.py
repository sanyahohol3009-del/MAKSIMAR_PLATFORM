from __future__ import annotations

from MAKSIMAR_CORE_LIB.evolution_debug import (
    build_debug_ranking_contract,
)


def test_debug_ranking_contract_builds() -> None:
    """Debug ranking contract should build successfully."""
    contract = build_debug_ranking_contract()

    assert contract.total_entries == 2
    assert len(contract.entries) == 2
    assert contract.proposal_ready is True


def test_debug_ranking_contract_is_ranked() -> None:
    """Debug ranking contract should keep deterministic ranks."""
    contract = build_debug_ranking_contract()

    assert contract.entries[0].rank == 1
    assert contract.entries[-1].rank == 2
    assert contract.entries[0].score >= contract.entries[-1].score

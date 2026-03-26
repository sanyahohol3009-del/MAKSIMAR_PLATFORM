from __future__ import annotations

from MAKSIMAR_CORE_LIB.evolution_debug.ranking_models import (
    DebugRankingContract,
    DebugRankingEntry,
)


def build_debug_ranking_contract() -> DebugRankingContract:
    """Build unified debug ranking contract."""

    entries = (
        DebugRankingEntry(
            rank=1,
            patch_id="patch_001",
            score=95,
            eligible_for_proposal=True,
        ),
        DebugRankingEntry(
            rank=2,
            patch_id="patch_002",
            score=91,
            eligible_for_proposal=True,
        ),
    )

    proposal_ready = any(entry.eligible_for_proposal for entry in entries)

    return DebugRankingContract(
        total_entries=len(entries),
        entries=entries,
        proposal_ready=proposal_ready,
    )

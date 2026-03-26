from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class DebugRankingEntry:
    """One ranked patch candidate after sandbox evaluation."""

    rank: int
    patch_id: str
    score: int
    eligible_for_proposal: bool


@dataclass(frozen=True, slots=True)
class DebugRankingContract:
    """Unified ranking contract for evolution debug layer."""

    total_entries: int
    entries: tuple[DebugRankingEntry, ...]
    proposal_ready: bool

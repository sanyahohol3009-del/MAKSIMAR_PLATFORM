from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class DebugProposalPackage:
    """One proposal package produced by evolution debug layer."""

    proposal_id: str
    selected_patch_id: str
    selected_rank: int
    sandbox_verified: bool
    approval_required: bool


@dataclass(frozen=True, slots=True)
class DebugProposalContract:
    """Unified proposal contract for evolution debug layer."""

    total_proposals: int
    proposals: tuple[DebugProposalPackage, ...]
    deploy_allowed: bool

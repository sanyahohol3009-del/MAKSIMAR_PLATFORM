from __future__ import annotations

from MAKSIMAR_CORE_LIB.evolution_debug.proposal_models import (
    DebugProposalContract,
    DebugProposalPackage,
)


def build_debug_proposal_contract() -> DebugProposalContract:
    """Build unified proposal contract."""

    proposals = (
        DebugProposalPackage(
            proposal_id="debug_proposal_001",
            selected_patch_id="patch_001",
            selected_rank=1,
            sandbox_verified=True,
            approval_required=True,
        ),
    )

    return DebugProposalContract(
        total_proposals=len(proposals),
        proposals=proposals,
        deploy_allowed=False,
    )

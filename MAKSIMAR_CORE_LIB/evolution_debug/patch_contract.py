from __future__ import annotations

from MAKSIMAR_CORE_LIB.evolution_debug.patch_models import (
    PatchCandidate,
    PatchCandidateContract,
)


def build_patch_candidate_contract() -> PatchCandidateContract:
    """Build unified patch candidate contract."""

    candidates = (
        PatchCandidate(
            patch_id="patch_001",
            hypothesis_id="hypothesis_001",
            patch_scope="runtime_observability",
            sandbox_only=True,
            core_write_allowed=False,
        ),
        PatchCandidate(
            patch_id="patch_002",
            hypothesis_id="hypothesis_002",
            patch_scope="oob_dashboard",
            sandbox_only=True,
            core_write_allowed=False,
        ),
    )

    return PatchCandidateContract(
        total_candidates=len(candidates),
        candidates=candidates,
        auto_deploy_allowed=False,
    )

from __future__ import annotations

from MAKSIMAR_CORE_LIB.evolution_debug.hypothesis_models import (
    DebugHypothesis,
    DebugHypothesisContract,
)


def build_debug_hypothesis_contract() -> DebugHypothesisContract:
    """Build unified debug hypothesis contract."""

    hypotheses = (
        DebugHypothesis(
            hypothesis_id="hypothesis_001",
            error_code="runtime.contract.mismatch",
            reasoning_summary="Runtime contract values diverge from expected source-of-truth semantics.",
            proposed_patch_scope="runtime_observability",
        ),
        DebugHypothesis(
            hypothesis_id="hypothesis_002",
            error_code="dashboard.binding.mismatch",
            reasoning_summary="Dashboard panel binding does not align with normalized panel identifiers.",
            proposed_patch_scope="oob_dashboard",
        ),
    )

    return DebugHypothesisContract(
        total_hypotheses=len(hypotheses),
        hypotheses=hypotheses,
        sandbox_required=True,
    )

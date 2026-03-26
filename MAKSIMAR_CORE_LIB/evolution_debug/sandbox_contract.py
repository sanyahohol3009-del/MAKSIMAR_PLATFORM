from __future__ import annotations

from MAKSIMAR_CORE_LIB.evolution_debug.sandbox_models import (
    SandboxEvaluation,
    SandboxEvaluationContract,
)


def build_sandbox_evaluation_contract() -> SandboxEvaluationContract:
    """Build unified sandbox evaluation contract."""

    evaluations = (
        SandboxEvaluation(
            evaluation_id="sandbox_eval_001",
            patch_id="patch_001",
            sandbox_executed=True,
            tests_passed=True,
            core_write_allowed=False,
        ),
        SandboxEvaluation(
            evaluation_id="sandbox_eval_002",
            patch_id="patch_002",
            sandbox_executed=True,
            tests_passed=True,
            core_write_allowed=False,
        ),
    )

    return SandboxEvaluationContract(
        total_evaluations=len(evaluations),
        evaluations=evaluations,
        deploy_allowed=False,
    )

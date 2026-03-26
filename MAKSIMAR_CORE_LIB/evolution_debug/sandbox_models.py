from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class SandboxEvaluation:
    """One sandbox evaluation result for a patch candidate."""

    evaluation_id: str
    patch_id: str
    sandbox_executed: bool
    tests_passed: bool
    core_write_allowed: bool


@dataclass(frozen=True, slots=True)
class SandboxEvaluationContract:
    """Unified sandbox evaluation contract for evolution debug layer."""

    total_evaluations: int
    evaluations: tuple[SandboxEvaluation, ...]
    deploy_allowed: bool

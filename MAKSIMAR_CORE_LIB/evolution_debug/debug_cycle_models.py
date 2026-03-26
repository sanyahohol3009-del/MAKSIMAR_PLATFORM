from __future__ import annotations

from dataclasses import dataclass
from typing import Literal


DebugStage = Literal[
    "error_detected",
    "reasoning",
    "hypothesis",
    "patch_prepared",
    "test_executed",
    "evaluation_completed",
    "ranking_completed",
    "proposal_ready",
]


@dataclass(frozen=True, slots=True)
class DebugCycleStage:
    """One stage inside controlled evolution debug cycle."""

    stage_name: DebugStage
    completed: bool


@dataclass(frozen=True, slots=True)
class EvolutionDebugCycle:
    """Unified debug cycle contract for controlled evolution."""

    cycle_id: str
    total_stages: int
    stages: tuple[DebugCycleStage, ...]
    sandbox_required: bool
    core_write_allowed: bool
    auto_deploy_allowed: bool

from __future__ import annotations

from MAKSIMAR_CORE_LIB.evolution_debug import (
    DebugCycleStage,
    EvolutionDebugCycle,
)


def test_debug_cycle_models_build() -> None:
    """Evolution debug cycle models should build successfully."""
    cycle = EvolutionDebugCycle(
        cycle_id="debug_cycle_001",
        total_stages=2,
        stages=(
            DebugCycleStage(stage_name="error_detected", completed=True),
            DebugCycleStage(stage_name="reasoning", completed=False),
        ),
        sandbox_required=True,
        core_write_allowed=False,
        auto_deploy_allowed=False,
    )

    assert cycle.cycle_id == "debug_cycle_001"
    assert cycle.total_stages == 2
    assert len(cycle.stages) == 2
    assert cycle.sandbox_required is True
    assert cycle.core_write_allowed is False
    assert cycle.auto_deploy_allowed is False

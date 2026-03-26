from __future__ import annotations

from MAKSIMAR_CORE_LIB.execution_control import (
    DegradedRuntimeContract,
    DegradedRuntimeState,
)


def test_degraded_runtime_models_build() -> None:
    """Degraded runtime models should build successfully."""
    contract = DegradedRuntimeContract(
        total_modes=2,
        modes=(
            DegradedRuntimeState(
                mode_id="degraded_001",
                active=False,
                disabled_feature="voice_duplex",
                reason="normal_operation",
            ),
            DegradedRuntimeState(
                mode_id="degraded_002",
                active=True,
                disabled_feature="background_indexing",
                reason="memory_pressure",
            ),
        ),
    )

    assert contract.total_modes == 2
    assert len(contract.modes) == 2
    assert contract.modes[0].disabled_feature == "voice_duplex"
    assert contract.modes[-1].active is True

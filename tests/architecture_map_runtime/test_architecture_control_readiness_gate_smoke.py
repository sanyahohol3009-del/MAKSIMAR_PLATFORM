from __future__ import annotations

from MAKSIMAR_SERVER.architecture_map_runtime import (
    build_architecture_control_phase_readiness,
)


def test_architecture_control_readiness_gate_smoke() -> None:
    readiness = build_architecture_control_phase_readiness()

    assert readiness.phase_ready is True
    assert readiness.architecture_shell_ready is True
    assert readiness.memory_architecture_binding_ready is True
    assert readiness.memory_data_flow_ready is True
    assert readiness.jarvis_memory_locator_ready is True
    assert readiness.domain_cube_memory_locator_ready is True

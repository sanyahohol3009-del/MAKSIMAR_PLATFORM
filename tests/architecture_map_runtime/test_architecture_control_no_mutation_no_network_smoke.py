from __future__ import annotations

from MAKSIMAR_SERVER.architecture_map_runtime import (
    build_architecture_control_phase_readiness,
)


def test_architecture_control_no_mutation_no_network_smoke() -> None:
    readiness = build_architecture_control_phase_readiness()

    assert readiness.read_only is True
    assert readiness.no_mutation_surface is True
    assert readiness.no_network_surface is True
    assert readiness.backend_execution_allowed is False

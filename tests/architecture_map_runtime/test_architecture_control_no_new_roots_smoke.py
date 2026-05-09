from __future__ import annotations

from MAKSIMAR_SERVER.architecture_map_runtime import (
    build_architecture_control_phase_readiness,
)


def test_architecture_control_no_new_roots_smoke() -> None:
    readiness = build_architecture_control_phase_readiness()

    assert readiness.no_new_architecture_root is True
    assert readiness.no_platform_inspector_root is True

from __future__ import annotations

from MAKSIMAR_SERVER.architecture_map_runtime import (
    build_domain_cube_memory_locator_contract,
    build_memory_dependency_summary,
)


def test_domain_cube_memory_locator_smoke() -> None:
    contract = build_domain_cube_memory_locator_contract()
    summary = build_memory_dependency_summary()

    assert contract.total_cubes >= 1
    assert contract.ready_cubes == contract.total_cubes
    assert contract.dashboard_visible_cubes == contract.total_cubes
    assert summary["phase_ready"] is True
    assert summary["no_new_architecture_root"] is True
    assert summary["no_platform_inspector_root"] is True

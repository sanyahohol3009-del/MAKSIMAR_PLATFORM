from __future__ import annotations

from MAKSIMAR_CORE_LIB.skill_domain_binding import build_cube_binding_contract


def test_cube_binding_models_smoke() -> None:
    contract = build_cube_binding_contract()

    assert contract.total_cubes == 16
    assert contract.ready_cubes == contract.total_cubes
    assert contract.dashboard_visible_cubes == contract.total_cubes
    assert contract.locator_ready_cubes == contract.total_cubes
    assert contract.source_exists_cubes == contract.total_cubes

    cube_slugs = {entry.cube_slug for entry in contract.entries}

    assert "3d_cube" in cube_slugs
    assert "cube_3d_cube" not in cube_slugs

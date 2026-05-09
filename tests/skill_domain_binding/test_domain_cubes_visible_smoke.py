from __future__ import annotations

from MAKSIMAR_CORE_LIB.skill_domain_binding import (
    build_cube_binding_contract,
    build_skill_domain_preview,
)


def test_domain_cubes_visible_smoke() -> None:
    cubes = build_cube_binding_contract()
    preview = build_skill_domain_preview()

    assert cubes.total_cubes == 16
    assert cubes.ready_cubes == cubes.total_cubes
    assert cubes.dashboard_visible_cubes == cubes.total_cubes
    assert cubes.source_exists_cubes == cubes.total_cubes

    cube_slugs = tuple(entry.cube_slug for entry in cubes.entries)

    assert "3d_cube" in cube_slugs
    assert "cube_3d_cube" not in cube_slugs
    assert "mobile_assistant_cube" in cube_slugs
    assert "visual_engineering_cube" in cube_slugs
    assert "robotics_cube" in cube_slugs
    assert "family_assistant" in cube_slugs

    assert preview["domain_cubes"] == 16
    assert preview["domain_cubes_ready"] == 16
    assert preview["domain_cubes_dashboard_visible"] == 16

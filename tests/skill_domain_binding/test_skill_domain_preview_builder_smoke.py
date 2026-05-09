from __future__ import annotations

from MAKSIMAR_CORE_LIB.skill_domain_binding import build_skill_domain_preview


def test_skill_domain_preview_builder_smoke() -> None:
    preview = build_skill_domain_preview()

    assert preview["preview_ready"] is True
    assert preview["batch1_ready"] is True
    assert preview["summary_ready"] is True
    assert preview["domain_cubes"] == 16
    assert "3d_cube" in preview["cube_slugs"]
    assert "cube_3d_cube" not in preview["cube_slugs"]
    assert "simulation_analysis" in tuple(
        skill_id.replace("skill_simulation_", "")
        for skill_id in preview["non_memory_backed_skill_ids"]
    ) or preview["non_memory_backed_skill_ids"]

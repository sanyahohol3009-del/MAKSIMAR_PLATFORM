from __future__ import annotations

from MAKSIMAR_CORE_LIB.skill_domain_binding import (
    build_cube_binding_contract,
    build_domain_layer_binding_contract,
    build_skill_binding_contract,
)


def test_phase_2_4_batch1_ready_smoke() -> None:
    skills = build_skill_binding_contract()
    cubes = build_cube_binding_contract()
    layers = build_domain_layer_binding_contract()

    assert skills.ready_bindings == skills.total_bindings
    assert cubes.ready_cubes == cubes.total_cubes
    assert layers.ready_layers == layers.total_layers

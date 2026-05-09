from __future__ import annotations

from MAKSIMAR_CORE_LIB.skill_domain_binding import (
    build_cube_binding_contract,
    build_domain_layer_binding_contract,
    build_shell_adapter_binding_contract,
    build_skill_binding_contract,
    build_skill_domain_preview,
    build_skill_domain_summary,
    build_skill_to_dashboard_binding_contract,
    build_skill_to_memory_binding_contract,
    build_skill_to_retrieval_binding_contract,
)


def test_skill_domain_binding_ready_smoke() -> None:
    skills = build_skill_binding_contract()
    cubes = build_cube_binding_contract()
    layers = build_domain_layer_binding_contract()
    shells = build_shell_adapter_binding_contract()
    memory = build_skill_to_memory_binding_contract()
    retrieval = build_skill_to_retrieval_binding_contract()
    dashboard = build_skill_to_dashboard_binding_contract()
    summary = build_skill_domain_summary()
    preview = build_skill_domain_preview()

    assert skills.ready_bindings == skills.total_bindings
    assert skills.manifest_bound_bindings == skills.total_bindings
    assert skills.registry_bound_bindings == skills.total_bindings
    assert skills.retrieval_reference_bound_bindings == skills.total_bindings
    assert skills.dashboard_reference_bound_bindings == skills.total_bindings

    assert cubes.ready_cubes == cubes.total_cubes
    assert cubes.dashboard_visible_cubes == cubes.total_cubes
    assert cubes.source_exists_cubes == cubes.total_cubes

    assert layers.ready_layers == layers.total_layers
    assert layers.registry_backed_layers == layers.total_layers
    assert layers.dashboard_visible_layers == layers.total_layers
    assert layers.read_only_layers == layers.total_layers

    assert shells.ready_bindings == shells.total_bindings
    assert shells.action_execution_allowed_bindings == 0

    assert memory.ready_bindings == memory.total_bindings
    assert memory.non_memory_backed_bindings >= 1

    assert retrieval.ready_bindings == retrieval.total_bindings
    assert retrieval.backend_execution_allowed_bindings == 0
    assert retrieval.mgrep_blocked_bindings == retrieval.total_bindings
    assert retrieval.sqlite_vec_blocked_bindings == retrieval.total_bindings

    assert dashboard.ready_bindings == dashboard.total_bindings
    assert dashboard.action_execution_allowed_bindings == 0

    assert summary["summary_ready"] is True
    assert preview["preview_ready"] is True
    assert preview["summary_ready"] is True
    assert preview["batch1_ready"] is True

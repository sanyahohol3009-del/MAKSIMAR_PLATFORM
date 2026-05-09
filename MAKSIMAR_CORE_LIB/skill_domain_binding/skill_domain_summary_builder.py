from __future__ import annotations

from typing import Dict

from MAKSIMAR_CORE_LIB.skill_domain_binding.cube_binding_models import (
    build_cube_binding_contract,
)
from MAKSIMAR_CORE_LIB.skill_domain_binding.domain_layer_binding_models import (
    build_domain_layer_binding_contract,
)
from MAKSIMAR_CORE_LIB.skill_domain_binding.skill_binding_models import (
    build_skill_binding_contract,
)
from MAKSIMAR_CORE_LIB.skill_domain_binding.shell_adapter_binding_models import (
    build_shell_adapter_binding_contract,
)
from MAKSIMAR_CORE_LIB.skill_domain_binding.skill_to_dashboard_binding_builder import (
    build_skill_to_dashboard_binding_contract,
)
from MAKSIMAR_CORE_LIB.skill_domain_binding.skill_to_memory_binding_builder import (
    build_skill_to_memory_binding_contract,
)
from MAKSIMAR_CORE_LIB.skill_domain_binding.skill_to_retrieval_binding_builder import (
    build_skill_to_retrieval_binding_contract,
)


def build_skill_domain_summary() -> Dict[str, object]:
    skills = build_skill_binding_contract()
    cubes = build_cube_binding_contract()
    layers = build_domain_layer_binding_contract()

    shells = build_shell_adapter_binding_contract()
    memory = build_skill_to_memory_binding_contract()
    retrieval = build_skill_to_retrieval_binding_contract()
    dashboard = build_skill_to_dashboard_binding_contract()

    summary_ready = (
        skills.ready_bindings == skills.total_bindings
        and skills.manifest_bound_bindings == skills.total_bindings
        and skills.registry_bound_bindings == skills.total_bindings
        and skills.retrieval_reference_bound_bindings == skills.total_bindings
        and skills.dashboard_reference_bound_bindings == skills.total_bindings
        and cubes.ready_cubes == cubes.total_cubes
        and cubes.dashboard_visible_cubes == cubes.total_cubes
        and cubes.source_exists_cubes == cubes.total_cubes
        and layers.ready_layers == layers.total_layers
        and layers.registry_backed_layers == layers.total_layers
        and layers.dashboard_visible_layers == layers.total_layers
        and layers.read_only_layers == layers.total_layers
        and shells.ready_bindings == shells.total_bindings
        and shells.action_execution_allowed_bindings == 0
        and memory.ready_bindings == memory.total_bindings
        and retrieval.ready_bindings == retrieval.total_bindings
        and retrieval.backend_execution_allowed_bindings == 0
        and dashboard.ready_bindings == dashboard.total_bindings
        and dashboard.action_execution_allowed_bindings == 0
    )

    return {
        "skill_bindings": skills.total_bindings,
        "skill_ready_bindings": skills.ready_bindings,
        "skill_manifest_bound_bindings": skills.manifest_bound_bindings,
        "skill_registry_bound_bindings": skills.registry_bound_bindings,
        "skill_memory_reference_bound_bindings": skills.memory_reference_bound_bindings,
        "skill_retrieval_reference_bound_bindings": skills.retrieval_reference_bound_bindings,
        "skill_dashboard_reference_bound_bindings": skills.dashboard_reference_bound_bindings,
        "engine_adapter_required_bindings": skills.engine_adapter_required_bindings,
        "domain_cubes": cubes.total_cubes,
        "domain_cubes_ready": cubes.ready_cubes,
        "domain_cubes_dashboard_visible": cubes.dashboard_visible_cubes,
        "domain_cubes_with_skill_binding": cubes.skill_binding_present_cubes,
        "domain_layers": layers.total_layers,
        "domain_layers_ready": layers.ready_layers,
        "domain_layers_dashboard_visible": layers.dashboard_visible_layers,
        "domain_layers_read_only": layers.read_only_layers,
        "shell_adapter_bindings": shells.total_bindings,
        "shell_adapter_ready_bindings": shells.ready_bindings,
        "shell_action_execution_allowed_bindings": shells.action_execution_allowed_bindings,
        "skill_to_memory_bindings": memory.total_bindings,
        "skill_to_memory_ready_bindings": memory.ready_bindings,
        "skill_to_memory_required_bindings": memory.memory_required_bindings,
        "skill_to_memory_non_memory_backed_bindings": memory.non_memory_backed_bindings,
        "skill_to_retrieval_bindings": retrieval.total_bindings,
        "skill_to_retrieval_ready_bindings": retrieval.ready_bindings,
        "skill_to_retrieval_backend_execution_allowed_bindings": retrieval.backend_execution_allowed_bindings,
        "skill_to_dashboard_bindings": dashboard.total_bindings,
        "skill_to_dashboard_ready_bindings": dashboard.ready_bindings,
        "skill_to_dashboard_action_execution_allowed_bindings": dashboard.action_execution_allowed_bindings,
        "summary_ready": summary_ready,
    }

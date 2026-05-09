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
from MAKSIMAR_CORE_LIB.skill_domain_binding.skill_domain_summary_builder import (
    build_skill_domain_summary,
)


_SKILL_DOMAIN_PREVIEW_FLOW = (
    "module_manifest",
    "skill_adapter_registry",
    "memory_registry",
    "retrieval_orchestration",
    "dashboard_read_only_views",
    "domain_cube_locator",
    "skill_binding",
    "cube_binding",
    "domain_layer_binding",
    "shell_adapter_binding",
    "skill_to_memory_binding",
    "skill_to_retrieval_binding",
    "skill_to_dashboard_binding",
    "skill_domain_preview",
)


def build_skill_domain_preview() -> Dict[str, object]:
    skills = build_skill_binding_contract()
    cubes = build_cube_binding_contract()
    layers = build_domain_layer_binding_contract()
    summary = build_skill_domain_summary()

    return {
        "flow": _SKILL_DOMAIN_PREVIEW_FLOW,
        "preview_ready": True,
        "batch1_ready": bool(summary["summary_ready"]),
        "summary_ready": summary["summary_ready"],
        "skill_bindings": summary["skill_bindings"],
        "skill_ready_bindings": summary["skill_ready_bindings"],
        "skill_memory_reference_bound_bindings": summary["skill_memory_reference_bound_bindings"],
        "skill_retrieval_reference_bound_bindings": summary["skill_retrieval_reference_bound_bindings"],
        "skill_dashboard_reference_bound_bindings": summary["skill_dashboard_reference_bound_bindings"],
        "domain_cubes": summary["domain_cubes"],
        "domain_cubes_ready": summary["domain_cubes_ready"],
        "domain_cubes_dashboard_visible": summary["domain_cubes_dashboard_visible"],
        "domain_cubes_with_skill_binding": summary["domain_cubes_with_skill_binding"],
        "domain_layers": summary["domain_layers"],
        "domain_layers_ready": summary["domain_layers_ready"],
        "domain_layers_dashboard_visible": summary["domain_layers_dashboard_visible"],
        "domain_layers_read_only": summary["domain_layers_read_only"],
        "shell_adapter_bindings": summary["shell_adapter_bindings"],
        "shell_adapter_ready_bindings": summary["shell_adapter_ready_bindings"],
        "shell_action_execution_allowed_bindings": summary["shell_action_execution_allowed_bindings"],
        "skill_to_memory_bindings": summary["skill_to_memory_bindings"],
        "skill_to_memory_ready_bindings": summary["skill_to_memory_ready_bindings"],
        "skill_to_memory_required_bindings": summary["skill_to_memory_required_bindings"],
        "skill_to_memory_non_memory_backed_bindings": summary["skill_to_memory_non_memory_backed_bindings"],
        "skill_to_retrieval_bindings": summary["skill_to_retrieval_bindings"],
        "skill_to_retrieval_ready_bindings": summary["skill_to_retrieval_ready_bindings"],
        "skill_to_retrieval_backend_execution_allowed_bindings": summary["skill_to_retrieval_backend_execution_allowed_bindings"],
        "skill_to_dashboard_bindings": summary["skill_to_dashboard_bindings"],
        "skill_to_dashboard_ready_bindings": summary["skill_to_dashboard_ready_bindings"],
        "skill_to_dashboard_action_execution_allowed_bindings": summary["skill_to_dashboard_action_execution_allowed_bindings"],
        "skill_ids": tuple(entry.skill_id for entry in skills.entries),
        "cube_slugs": tuple(entry.cube_slug for entry in cubes.entries),
        "layer_kinds": tuple(entry.layer_kind for entry in layers.entries),
        "non_memory_backed_skill_ids": tuple(
            entry.skill_id for entry in skills.entries if not entry.memory_reference_bound
        ),
    }

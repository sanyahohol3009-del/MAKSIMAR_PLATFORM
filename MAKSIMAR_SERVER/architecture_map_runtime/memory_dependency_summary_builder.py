from __future__ import annotations

from typing import Dict

from MAKSIMAR_SERVER.architecture_map_runtime.domain_cube_memory_locator import (
    build_domain_cube_memory_locator_contract,
)
from MAKSIMAR_SERVER.architecture_map_runtime.jarvis_memory_locator import (
    build_jarvis_memory_locator_contract,
)
from MAKSIMAR_SERVER.architecture_map_runtime.memory_data_flow_binding import (
    build_memory_data_flow_binding_contract,
)
from MAKSIMAR_SERVER.architecture_map_runtime.memory_layer_architecture_binding import (
    build_memory_layer_architecture_binding_contract,
)
from MAKSIMAR_SERVER.architecture_map_runtime.server_architecture_shell_contract import (
    build_server_architecture_map_shell_contract,
)


def build_memory_dependency_summary() -> Dict[str, object]:
    shell = build_server_architecture_map_shell_contract()
    architecture_binding = build_memory_layer_architecture_binding_contract()
    data_flow = build_memory_data_flow_binding_contract()
    jarvis_locator = build_jarvis_memory_locator_contract()
    domain_cube_locator = build_domain_cube_memory_locator_contract()

    phase_ready = (
        architecture_binding.ready_bindings == architecture_binding.total_bindings
        and data_flow.ready_flows == data_flow.total_flows
        and jarvis_locator.ready_locators == jarvis_locator.total_locators
        and domain_cube_locator.ready_cubes == domain_cube_locator.total_cubes
    )

    return {
        "architecture_shell_id": shell.shell_id,
        "architecture_module_views": shell.total_module_views,
        "architecture_dependency_views": shell.total_dependency_views,
        "architecture_flow_views": shell.total_flow_views,
        "memory_architecture_bindings": architecture_binding.total_bindings,
        "memory_data_flows": data_flow.total_flows,
        "jarvis_memory_locators": jarvis_locator.total_locators,
        "domain_cube_memory_locators": domain_cube_locator.total_cubes,
        "read_only": True,
        "source_contract_bound": True,
        "no_new_architecture_root": True,
        "no_platform_inspector_root": True,
        "phase_ready": phase_ready,
    }

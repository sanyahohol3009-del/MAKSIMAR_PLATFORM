from __future__ import annotations

from MAKSIMAR_SERVER.architecture_map_runtime.dependency_view_contract import (
    build_server_dependency_view_contract,
)
from MAKSIMAR_SERVER.architecture_map_runtime.flow_view_contract import (
    build_server_flow_view_contract,
)
from MAKSIMAR_SERVER.architecture_map_runtime.module_view_contract import (
    build_server_module_view_contract,
)
from MAKSIMAR_SERVER.architecture_map_runtime.server_architecture_shell_models import (
    ServerArchitectureMapShellContract,
)


def build_server_architecture_map_shell_contract() -> (
    ServerArchitectureMapShellContract
):
    """Build final shell contract for server-side architecture map layer."""
    module_views = build_server_module_view_contract()
    dependency_views = build_server_dependency_view_contract()
    flow_views = build_server_flow_view_contract()

    return ServerArchitectureMapShellContract(
        shell_id="server_architecture_map_shell",
        total_module_views=module_views.total_modules,
        total_dependency_views=dependency_views.total_edges,
        total_flow_views=flow_views.total_steps,
    )

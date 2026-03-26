from __future__ import annotations

from MAKSIMAR_CORE_LIB.architecture_map import (
    build_module_registry_contract,
)
from MAKSIMAR_SERVER.architecture_map_runtime.module_view_models import (
    ServerModuleViewContract,
    ServerModuleViewEntry,
)


def build_server_module_view_contract() -> ServerModuleViewContract:
    """Build unified server-side module view contract."""
    registry = build_module_registry_contract()

    modules = tuple(
        ServerModuleViewEntry(
            module_id=module.module_id,
            layer_name=module.layer_name,
            criticality=module.criticality,
            dashboard_visible=module.read_only_view_available,
            source_contract_bound=True,
        )
        for module in registry.modules
    )

    return ServerModuleViewContract(
        total_modules=len(modules),
        modules=modules,
    )

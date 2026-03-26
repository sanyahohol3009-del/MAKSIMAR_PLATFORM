from __future__ import annotations

from MAKSIMAR_CORE_LIB.architecture_map.module_registry_models import (
    ModuleRegistryContract,
    ModuleRegistryEntry,
)


def build_module_registry_contract() -> ModuleRegistryContract:
    """Build unified canonical module registry contract."""

    modules = (
        ModuleRegistryEntry(
            module_id="control_plane",
            layer_name="server_control",
            criticality="high",
            read_only_view_available=True,
        ),
        ModuleRegistryEntry(
            module_id="execution_control",
            layer_name="server_execution",
            criticality="high",
            read_only_view_available=True,
        ),
        ModuleRegistryEntry(
            module_id="oob_dashboard",
            layer_name="read_only_ui",
            criticality="medium",
            read_only_view_available=True,
        ),
    )

    return ModuleRegistryContract(
        total_modules=len(modules),
        modules=modules,
    )

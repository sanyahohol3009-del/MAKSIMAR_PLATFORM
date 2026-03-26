from __future__ import annotations

from MAKSIMAR_CORE_LIB.architecture_map import (
    ModuleRegistryContract,
    ModuleRegistryEntry,
)


def test_module_registry_models_build() -> None:
    """Module registry models should build successfully."""
    contract = ModuleRegistryContract(
        total_modules=3,
        modules=(
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
        ),
    )

    assert contract.total_modules == 3
    assert len(contract.modules) == 3
    assert contract.modules[0].module_id == "control_plane"
    assert contract.modules[-1].module_id == "oob_dashboard"

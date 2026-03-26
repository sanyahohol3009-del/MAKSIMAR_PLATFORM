from __future__ import annotations

from MAKSIMAR_CORE_LIB.architecture_map import (
    CanonicalModuleIdentity,
    CanonicalModuleIdentityContract,
)


def test_module_identity_models_build() -> None:
    """Canonical module identity models should build successfully."""
    contract = CanonicalModuleIdentityContract(
        total_modules=4,
        modules=(
            CanonicalModuleIdentity(
                module_id="control_plane",
                layer_name="server_control",
            ),
            CanonicalModuleIdentity(
                module_id="execution_control",
                layer_name="server_execution",
            ),
            CanonicalModuleIdentity(
                module_id="execution_observability",
                layer_name="server_observability",
            ),
            CanonicalModuleIdentity(
                module_id="oob_dashboard",
                layer_name="read_only_ui",
            ),
        ),
    )

    assert contract.total_modules == 4
    assert len(contract.modules) == 4
    assert contract.modules[0].module_id == "control_plane"
    assert contract.modules[-1].module_id == "oob_dashboard"

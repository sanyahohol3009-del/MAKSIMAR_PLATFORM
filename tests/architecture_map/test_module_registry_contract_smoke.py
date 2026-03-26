from __future__ import annotations

from MAKSIMAR_CORE_LIB.architecture_map import (
    build_module_registry_contract,
)


def test_module_registry_contract_builds() -> None:
    """Module registry contract should build successfully."""
    contract = build_module_registry_contract()

    assert contract.total_modules == 3
    assert len(contract.modules) == 3


def test_module_registry_contract_contains_expected_modules() -> None:
    """Module registry contract should expose expected canonical modules."""
    contract = build_module_registry_contract()

    module_ids = {module.module_id for module in contract.modules}

    assert "control_plane" in module_ids
    assert "execution_control" in module_ids
    assert "oob_dashboard" in module_ids

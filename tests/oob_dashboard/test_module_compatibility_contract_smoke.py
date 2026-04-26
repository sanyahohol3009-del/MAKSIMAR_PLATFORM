from __future__ import annotations

import pytest

from MAKSIMAR_CORE_LIB.oob_dashboard.module_compatibility_contract import (
    ModuleCompatibilityContract,
    ModuleCompatibilityEntry,
    build_module_compatibility_contract,
)


def test_module_compatibility_contract_builds() -> None:
    contract = build_module_compatibility_contract()

    assert contract.contract_id == "module_compatibility_contract_001"
    assert contract.total_entries == 3
    assert contract.mount_eligible_entries == 3
    assert contract.permission_valid_entries == 3
    assert contract.compatible_entries == 3
    assert contract.operator_visible_entries == 3
    assert contract.truth_bound_entries == 3


def test_module_compatibility_contains_expected_entries() -> None:
    contract = build_module_compatibility_contract()
    entry_map = {entry.module_id: entry for entry in contract.entries}

    assert entry_map["module_manifest_001"].mount_eligible is True
    assert entry_map["module_manifest_002"].permission_valid is True
    assert entry_map["module_manifest_003"].compatible_with_base_family is True


def test_module_compatibility_entry_rejects_non_mount_eligible() -> None:
    with pytest.raises(
        ValueError,
        match="mount_eligible must remain true for canonical module compatibility entries.",
    ):
        ModuleCompatibilityEntry(
            compatibility_entry_id="bad_compatibility",
            module_id="module_manifest_001",
            mount_eligible=False,
            permission_valid=True,
            compatible_with_base_family=True,
            operator_visible=True,
            truth_bound=True,
            description="Invalid compatibility entry.",
        )


def test_module_compatibility_manual_contract_builds() -> None:
    entries = (
        ModuleCompatibilityEntry(
            compatibility_entry_id="module_compatibility_001",
            module_id="module_manifest_001",
            mount_eligible=True,
            permission_valid=True,
            compatible_with_base_family=True,
            operator_visible=True,
            truth_bound=True,
            description="Canonical compatibility entry.",
        ),
    )

    contract = ModuleCompatibilityContract(
        contract_id="module_compatibility_contract_001",
        total_entries=1,
        mount_eligible_entries=1,
        permission_valid_entries=1,
        compatible_entries=1,
        operator_visible_entries=1,
        truth_bound_entries=1,
        entries=entries,
    )

    assert contract.total_entries == 1

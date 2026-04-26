from __future__ import annotations

import pytest

from MAKSIMAR_CORE_LIB.oob_dashboard.module_permission_matrix_contract import (
    ModulePermissionMatrixContract,
    ModulePermissionMatrixEntry,
    build_module_permission_matrix_contract,
)


def test_module_permission_matrix_contract_builds() -> None:
    contract = build_module_permission_matrix_contract()

    assert contract.contract_id == "module_permission_matrix_contract_001"
    assert contract.total_entries == 3
    assert contract.approval_required_entries == 1
    assert contract.operator_visible_entries == 3
    assert contract.truth_bound_entries == 3


def test_module_permission_matrix_contains_expected_entries() -> None:
    contract = build_module_permission_matrix_contract()
    entry_map = {entry.module_id: entry for entry in contract.entries}

    assert entry_map["module_manifest_001"].permission_level == "read_only"
    assert entry_map["module_manifest_002"].permission_level == "operator_interaction"
    assert entry_map["module_manifest_003"].permission_level == "optional_extension"
    assert entry_map["module_manifest_003"].approval_required is True


def test_module_permission_entry_rejects_read_only_with_approval() -> None:
    with pytest.raises(
        ValueError,
        match="read_only permission entries must not require approval.",
    ):
        ModulePermissionMatrixEntry(
            permission_entry_id="bad_permission",
            module_id="module_manifest_001",
            permission_level="read_only",
            approval_required=True,
            operator_visible=True,
            truth_bound=True,
            description="Invalid permission entry.",
        )


def test_module_permission_manual_contract_builds() -> None:
    entries = (
        ModulePermissionMatrixEntry(
            permission_entry_id="module_permission_001",
            module_id="module_manifest_001",
            permission_level="read_only",
            approval_required=False,
            operator_visible=True,
            truth_bound=True,
            description="Canonical permission entry.",
        ),
    )

    contract = ModulePermissionMatrixContract(
        contract_id="module_permission_matrix_contract_001",
        total_entries=1,
        approval_required_entries=0,
        operator_visible_entries=1,
        truth_bound_entries=1,
        entries=entries,
    )

    assert contract.total_entries == 1

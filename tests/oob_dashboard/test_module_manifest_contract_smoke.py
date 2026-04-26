from __future__ import annotations

import pytest

from MAKSIMAR_CORE_LIB.oob_dashboard.module_manifest_contract import (
    ModuleManifestContract,
    ModuleManifestEntry,
    build_module_manifest_contract,
)


def test_module_manifest_contract_builds() -> None:
    contract = build_module_manifest_contract()

    assert contract.contract_id == "module_manifest_contract_001"
    assert contract.total_entries == 3
    assert contract.required_mount_entries == 2
    assert contract.optional_mount_entries == 1
    assert contract.operator_visible_entries == 3
    assert contract.truth_bound_entries == 3


def test_module_manifest_contains_expected_entries() -> None:
    contract = build_module_manifest_contract()
    entry_map = {entry.module_name: entry for entry in contract.entries}

    assert entry_map["foundation_monitoring_module"].mount_mode == "mount_required"
    assert entry_map["operator_interaction_module"].mount_mode == "mount_required"
    assert entry_map["optional_product_module"].mount_mode == "mount_optional"


def test_module_manifest_entry_rejects_non_truth_bound() -> None:
    with pytest.raises(
        ValueError,
        match="truth_bound must remain true for canonical module manifest entries.",
    ):
        ModuleManifestEntry(
            module_id="bad_module",
            module_name="bad_module",
            module_role="base_family_module",
            mount_mode="mount_required",
            allowed_workspace="workspace_foundation_monitoring",
            operator_visible=True,
            truth_bound=False,
            description="Invalid manifest entry.",
        )


def test_module_manifest_manual_contract_builds() -> None:
    entries = (
        ModuleManifestEntry(
            module_id="module_manifest_001",
            module_name="foundation_monitoring_module",
            module_role="base_family_module",
            mount_mode="mount_required",
            allowed_workspace="workspace_foundation_monitoring",
            operator_visible=True,
            truth_bound=True,
            description="Canonical manifest entry.",
        ),
    )

    contract = ModuleManifestContract(
        contract_id="module_manifest_contract_001",
        total_entries=1,
        required_mount_entries=1,
        optional_mount_entries=0,
        operator_visible_entries=1,
        truth_bound_entries=1,
        entries=entries,
    )

    assert contract.total_entries == 1

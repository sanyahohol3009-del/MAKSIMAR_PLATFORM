from __future__ import annotations

import pytest

from MAKSIMAR_CORE_LIB.oob_dashboard.visual_backend_import_policy_contract import (
    VisualBackendImportPolicyEntry,
    build_visual_backend_import_policy_contract,
)


def test_visual_backend_import_policy_contract_builds() -> None:
    contract = build_visual_backend_import_policy_contract()

    assert contract.contract_id == "visual_backend_import_policy_contract_001"
    assert contract.total_entries == 4
    assert contract.adapter_boundary_required_entries == 4
    assert contract.canonical_id_only_entries == 4
    assert contract.swap_safe_entries == 4
    assert contract.operator_visible_entries == 4
    assert contract.truth_bound_entries == 4


def test_visual_backend_import_policy_contract_contains_expected_layers() -> None:
    contract = build_visual_backend_import_policy_contract()

    values = tuple(
        (entry.policy_entry_id, entry.protected_layer, entry.swap_safe)
        for entry in contract.entries
    )

    assert values == (
        ("visual_backend_import_policy_001", "canonical_contract_layer", True),
        ("visual_backend_import_policy_002", "read_model_layer", True),
        ("visual_backend_import_policy_003", "preview_contract_layer", True),
        ("visual_backend_import_policy_004", "visual_family_projection_layer", True),
    )


def test_visual_backend_import_policy_entry_rejects_direct_oss_import() -> None:
    with pytest.raises(
        ValueError,
        match="direct_oss_import_allowed must remain false for canonical visual backend import policy entries.",
    ):
        VisualBackendImportPolicyEntry(
            policy_entry_id="bad_import_policy",
            protected_layer="canonical_contract_layer",
            direct_oss_import_allowed=True,
            adapter_boundary_required=True,
            canonical_id_only=True,
            swap_safe=True,
            operator_visible=True,
            truth_bound=True,
            description="Invalid import policy entry.",
        )

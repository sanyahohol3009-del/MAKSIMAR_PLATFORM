from __future__ import annotations

import pytest

from MAKSIMAR_CORE_LIB.oob_dashboard.visual_backend_path_replaceability_contract import (
    VisualBackendPathReplaceabilityEntry,
    build_visual_backend_path_replaceability_contract,
)


def test_visual_backend_path_replaceability_contract_builds() -> None:
    contract = build_visual_backend_path_replaceability_contract()

    assert contract.contract_id == "visual_backend_path_replaceability_contract_001"
    assert contract.total_entries == 3
    assert contract.path_swap_safe_entries == 3
    assert contract.canonical_semantics_preserved_entries == 3
    assert contract.preview_consumer_compatible_entries == 3
    assert contract.operator_visible_entries == 3
    assert contract.truth_bound_entries == 3


def test_visual_backend_path_replaceability_contract_contains_expected_paths() -> None:
    contract = build_visual_backend_path_replaceability_contract()

    values = tuple(
        (
            entry.replaceability_entry_id,
            entry.canonical_path_id,
            entry.producer_contract_id,
            entry.consumer_contract_id,
        )
        for entry in contract.entries
    )

    assert values == (
        (
            "visual_backend_path_replaceability_001",
            "runtime_to_preview_path",
            "runtime_data_handoff_integration_contract_001",
            "preview_consumer_integration_contract_001",
        ),
        (
            "visual_backend_path_replaceability_002",
            "runtime_to_runtime_summary_path",
            "runtime_data_handoff_integration_contract_001",
            "visual_adapter_runtime_summary_surface",
        ),
        (
            "visual_backend_path_replaceability_003",
            "degraded_to_preview_path",
            "visual_degraded_mode_capability_contract_001",
            "preview_consumer_integration_contract_001",
        ),
    )


def test_visual_backend_path_replaceability_entry_rejects_read_model_change_requirement() -> None:
    with pytest.raises(
        ValueError,
        match="read_model_change_required must remain false for canonical visual backend path replaceability entries.",
    ):
        VisualBackendPathReplaceabilityEntry(
            replaceability_entry_id="bad_path_replaceability",
            canonical_path_id="bad_path",
            producer_contract_id="producer_a",
            consumer_contract_id="consumer_b",
            path_swap_safe=True,
            canonical_semantics_preserved=True,
            preview_consumer_compatible=True,
            contract_change_required=False,
            read_model_change_required=True,
            operator_visible=True,
            truth_bound=True,
            description="Invalid path replaceability entry.",
        )

from __future__ import annotations

import pytest

from MAKSIMAR_CORE_LIB.oob_dashboard.runtime_data_handoff_integration_contract import (
    RuntimeDataHandoffIntegrationEntry,
    build_runtime_data_handoff_integration_contract,
)


def test_runtime_data_handoff_integration_contract_builds() -> None:
    contract = build_runtime_data_handoff_integration_contract()

    assert contract.contract_id == "runtime_data_handoff_integration_contract_001"
    assert contract.total_entries == 3
    assert contract.payload_consistent_entries == 3
    assert contract.canonical_id_preserved_entries == 3
    assert contract.handoff_complete_entries == 3
    assert contract.operator_visible_entries == 3
    assert contract.truth_bound_entries == 3


def test_runtime_data_handoff_integration_contract_contains_expected_handoffs() -> None:
    contract = build_runtime_data_handoff_integration_contract()

    values = tuple(
        (entry.integration_entry_id, entry.producer_id, entry.consumer_id)
        for entry in contract.entries
    )

    assert values == (
        (
            "runtime_data_handoff_integration_001",
            "visual_capability_matrix_contract_001",
            "visual_backend_import_policy_contract_001",
        ),
        (
            "runtime_data_handoff_integration_002",
            "visual_backend_import_policy_contract_001",
            "replaceability_guard_preview_consumer",
        ),
        (
            "runtime_data_handoff_integration_003",
            "visual_capability_matrix_contract_001",
            "visual_adapter_runtime_summary",
        ),
    )


def test_runtime_data_handoff_integration_entry_rejects_incomplete_handoff() -> None:
    with pytest.raises(
        ValueError,
        match="handoff_complete must remain true for canonical runtime data handoff integration entries.",
    ):
        RuntimeDataHandoffIntegrationEntry(
            integration_entry_id="bad_runtime_handoff",
            producer_id="producer_a",
            consumer_id="consumer_b",
            handoff_scope="bad_scope",
            payload_consistent=True,
            canonical_id_preserved=True,
            handoff_complete=False,
            operator_visible=True,
            truth_bound=True,
            description="Invalid runtime handoff entry.",
        )

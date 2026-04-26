from __future__ import annotations

import pytest

from MAKSIMAR_CORE_LIB.oob_dashboard.preview_consumer_integration_contract import (
    PreviewConsumerIntegrationEntry,
    build_preview_consumer_integration_contract,
)


def test_preview_consumer_integration_contract_builds() -> None:
    contract = build_preview_consumer_integration_contract()

    assert contract.contract_id == "preview_consumer_integration_contract_001"
    assert contract.total_entries == 3
    assert contract.preview_ready_entries == 3
    assert contract.canonical_id_preserved_entries == 3
    assert contract.readable_operator_state_preserved_entries == 3
    assert contract.handoff_complete_entries == 3
    assert contract.operator_visible_entries == 3
    assert contract.truth_bound_entries == 3


def test_preview_consumer_integration_contract_contains_expected_consumers() -> None:
    contract = build_preview_consumer_integration_contract()

    values = tuple(
        (entry.integration_entry_id, entry.producer_contract_id, entry.consumer_surface_id)
        for entry in contract.entries
    )

    assert values == (
        (
            "preview_consumer_integration_001",
            "runtime_data_handoff_integration_contract_001",
            "runtime_data_handoff_preview_surface",
        ),
        (
            "preview_consumer_integration_002",
            "visual_degraded_mode_capability_contract_001",
            "degraded_capability_preview_surface",
        ),
        (
            "preview_consumer_integration_003",
            "runtime_data_handoff_integration_contract_001",
            "visual_adapter_runtime_summary_surface",
        ),
    )


def test_preview_consumer_integration_entry_rejects_unreadable_state() -> None:
    with pytest.raises(
        ValueError,
        match="readable_operator_state_preserved must remain true for canonical preview consumer integration entries.",
    ):
        PreviewConsumerIntegrationEntry(
            integration_entry_id="bad_preview_consumer",
            producer_contract_id="runtime_data_handoff_integration_contract_001",
            consumer_surface_id="bad_surface",
            preview_ready=True,
            canonical_id_preserved=True,
            readable_operator_state_preserved=False,
            handoff_complete=True,
            operator_visible=True,
            truth_bound=True,
            description="Invalid preview consumer entry.",
        )

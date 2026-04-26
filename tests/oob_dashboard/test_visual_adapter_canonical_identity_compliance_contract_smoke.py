from __future__ import annotations

import pytest

from MAKSIMAR_CORE_LIB.oob_dashboard.visual_adapter_canonical_identity_compliance_contract import (
    VisualAdapterCanonicalIdentityComplianceEntry,
    build_visual_adapter_canonical_identity_compliance_contract,
)


def test_visual_adapter_canonical_identity_compliance_contract_builds() -> None:
    contract = build_visual_adapter_canonical_identity_compliance_contract()

    assert contract.contract_id == "visual_adapter_canonical_identity_compliance_contract_001"
    assert contract.total_entries == 3
    assert contract.canonical_id_preserved_entries == 3
    assert contract.canonical_semantics_preserved_entries == 3
    assert contract.compliance_passed_entries == 3
    assert contract.operator_visible_entries == 3
    assert contract.truth_bound_entries == 3


def test_visual_adapter_canonical_identity_compliance_contract_contains_expected_scopes() -> None:
    contract = build_visual_adapter_canonical_identity_compliance_contract()

    values = tuple(
        (
            entry.compliance_entry_id,
            entry.producer_contract_id,
            entry.consumer_contract_id,
            entry.compliance_scope,
        )
        for entry in contract.entries
    )

    assert values == (
        (
            "visual_adapter_canonical_identity_compliance_001",
            "runtime_data_handoff_integration_contract_001",
            "visual_adapter_vendor_leakage_compliance_contract_001",
            "runtime_to_vendor_leakage_compliance",
        ),
        (
            "visual_adapter_canonical_identity_compliance_002",
            "preview_consumer_integration_contract_001",
            "visual_adapter_vendor_leakage_compliance_contract_001",
            "preview_to_vendor_leakage_compliance",
        ),
        (
            "visual_adapter_canonical_identity_compliance_003",
            "runtime_data_handoff_integration_contract_001",
            "preview_consumer_integration_contract_001",
            "runtime_to_preview_identity_compliance",
        ),
    )


def test_visual_adapter_canonical_identity_entry_rejects_semantic_drift() -> None:
    with pytest.raises(
        ValueError,
        match="canonical_semantics_preserved must remain true for canonical identity compliance entries.",
    ):
        VisualAdapterCanonicalIdentityComplianceEntry(
            compliance_entry_id="bad_identity_compliance",
            producer_contract_id="runtime_data_handoff_integration_contract_001",
            consumer_contract_id="preview_consumer_integration_contract_001",
            compliance_scope="bad_scope",
            canonical_id_preserved=True,
            canonical_semantics_preserved=False,
            compliance_passed=True,
            operator_visible=True,
            truth_bound=True,
            description="Invalid identity compliance entry.",
        )

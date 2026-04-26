from __future__ import annotations

import pytest

from MAKSIMAR_CORE_LIB.oob_dashboard.visual_adapter_vendor_leakage_compliance_contract import (
    VisualAdapterVendorLeakageComplianceEntry,
    build_visual_adapter_vendor_leakage_compliance_contract,
)


def test_visual_adapter_vendor_leakage_compliance_contract_builds() -> None:
    contract = build_visual_adapter_vendor_leakage_compliance_contract()

    assert contract.contract_id == "visual_adapter_vendor_leakage_compliance_contract_001"
    assert contract.total_entries == 4
    assert contract.compliance_passed_entries == 4
    assert contract.operator_visible_entries == 4
    assert contract.truth_bound_entries == 4


def test_visual_adapter_vendor_leakage_compliance_contract_contains_expected_scopes() -> None:
    contract = build_visual_adapter_vendor_leakage_compliance_contract()

    values = tuple(
        (entry.compliance_entry_id, entry.adapter_contract_id, entry.compliance_scope)
        for entry in contract.entries
    )

    assert values == (
        (
            "visual_adapter_vendor_leakage_compliance_001",
            "graph_render_adapter_contract_001",
            "graph_adapter_vendor_leakage",
        ),
        (
            "visual_adapter_vendor_leakage_compliance_002",
            "chart_render_adapter_contract_001",
            "chart_adapter_vendor_leakage",
        ),
        (
            "visual_adapter_vendor_leakage_compliance_003",
            "overlay_render_adapter_contract_001",
            "overlay_adapter_vendor_leakage",
        ),
        (
            "visual_adapter_vendor_leakage_compliance_004",
            "motion_render_adapter_contract_001",
            "motion_adapter_vendor_leakage",
        ),
    )


def test_visual_adapter_vendor_leakage_entry_rejects_vendor_payload_leakage() -> None:
    with pytest.raises(
        ValueError,
        match="vendor_payload_exposed must remain false for canonical visual adapter vendor leakage compliance entries.",
    ):
        VisualAdapterVendorLeakageComplianceEntry(
            compliance_entry_id="bad_vendor_leakage",
            adapter_contract_id="graph_render_adapter_contract_001",
            compliance_scope="bad_scope",
            vendor_identifier_exposed=False,
            vendor_payload_exposed=True,
            truth_leakage_allowed=False,
            compliance_passed=True,
            operator_visible=True,
            truth_bound=True,
            description="Invalid vendor leakage entry.",
        )

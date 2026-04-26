from __future__ import annotations

import pytest

from MAKSIMAR_CORE_LIB.oob_dashboard.visual_backend_replaceability_contract import (
    VisualBackendReplaceabilityEntry,
    build_visual_backend_replaceability_contract,
)


def test_visual_backend_replaceability_contract_builds() -> None:
    contract = build_visual_backend_replaceability_contract()

    assert contract.contract_id == "visual_backend_replaceability_contract_001"
    assert contract.total_entries == 4
    assert contract.swap_ready_entries == 4
    assert contract.replaceable_entries == 4
    assert contract.operator_visible_entries == 4
    assert contract.truth_bound_entries == 4


def test_visual_backend_replaceability_contract_contains_expected_ids() -> None:
    contract = build_visual_backend_replaceability_contract()

    values = tuple(
        (entry.replaceability_entry_id, entry.backend_id, entry.adapter_contract_id)
        for entry in contract.entries
    )

    assert values == (
        (
            "visual_backend_replaceability_001",
            "visual_backend_graph_001",
            "graph_render_adapter_contract_001",
        ),
        (
            "visual_backend_replaceability_002",
            "visual_backend_chart_001",
            "chart_render_adapter_contract_001",
        ),
        (
            "visual_backend_replaceability_003",
            "visual_backend_overlay_001",
            "overlay_render_adapter_contract_001",
        ),
        (
            "visual_backend_replaceability_004",
            "motion_backend_virtual_001",
            "motion_render_adapter_contract_001",
        ),
    )


def test_visual_backend_replaceability_entry_rejects_direct_vendor_dependency() -> None:
    with pytest.raises(
        ValueError,
        match="direct_vendor_dependency_allowed must remain false for canonical visual backend replaceability entries.",
    ):
        VisualBackendReplaceabilityEntry(
            replaceability_entry_id="bad_replaceability",
            backend_id="visual_backend_graph_001",
            adapter_contract_id="graph_render_adapter_contract_001",
            swap_ready=True,
            canonical_contract_change_required=False,
            read_model_change_required=False,
            direct_vendor_dependency_allowed=True,
            replaceable=True,
            operator_visible=True,
            truth_bound=True,
            description="Invalid replaceability entry.",
        )

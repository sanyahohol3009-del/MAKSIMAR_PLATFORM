from __future__ import annotations

import pytest

from MAKSIMAR_CORE_LIB.oob_dashboard.graph_selection_mapping_contract import (
    GraphSelectionMappingEntry,
    build_graph_selection_mapping_contract,
)


def test_graph_selection_mapping_contract_builds() -> None:
    contract = build_graph_selection_mapping_contract()

    assert contract.contract_id == "graph_selection_mapping_contract_001"
    assert contract.total_entries == 3
    assert contract.canonical_id_preserved_entries == 3
    assert contract.selection_mapping_ready_entries == 3
    assert contract.operator_visible_entries == 3
    assert contract.truth_bound_entries == 3


def test_graph_selection_mapping_contract_contains_expected_entries() -> None:
    contract = build_graph_selection_mapping_contract()

    values = tuple(
        (
            entry.selection_entry_id,
            entry.selection_scope,
            entry.selection_kind,
        )
        for entry in contract.entries
    )

    assert values == (
        (
            "graph_selection_mapping_001",
            "dependency_graph_selection",
            "dependency_projection",
        ),
        (
            "graph_selection_mapping_002",
            "dataflow_graph_selection",
            "dataflow_projection",
        ),
        (
            "graph_selection_mapping_003",
            "combined_graph_inspect_selection",
            "inspect_projection",
        ),
    )


def test_graph_selection_mapping_entry_rejects_vendor_selection_exposure() -> None:
    with pytest.raises(
        ValueError,
        match="vendor_selection_exposed must remain false for canonical graph selection mapping entries.",
    ):
        GraphSelectionMappingEntry(
            selection_entry_id="bad_selection_mapping",
            selection_scope="selection_scope",
            canonical_selection_id="selection_id",
            projection_target_id="projection_id",
            selection_kind="selection_kind",
            canonical_id_preserved=True,
            vendor_selection_exposed=True,
            selection_mapping_ready=True,
            operator_visible=True,
            truth_bound=True,
            description="Invalid graph selection mapping entry.",
        )

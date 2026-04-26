from __future__ import annotations

import pytest

from MAKSIMAR_CORE_LIB.oob_dashboard.graph_interaction_selection_contract import (
    GraphInteractionSelectionEntry,
    build_graph_interaction_selection_contract,
)


def test_graph_interaction_selection_contract_builds() -> None:
    contract = build_graph_interaction_selection_contract()

    assert contract.contract_id == "graph_interaction_selection_contract_001"
    assert contract.total_entries == 3
    assert contract.selection_ready_entries == 3
    assert contract.inspect_only_entries == 3
    assert contract.operator_visible_entries == 3
    assert contract.truth_bound_entries == 3


def test_graph_interaction_selection_contract_contains_expected_entries() -> None:
    contract = build_graph_interaction_selection_contract()

    values = tuple(
        (
            entry.selection_entry_id,
            entry.interaction_kind,
            entry.inspect_surface_id,
        )
        for entry in contract.entries
    )

    assert values == (
        (
            "graph_interaction_selection_001",
            "graph_select",
            "graph_inspect_primary_surface",
        ),
        (
            "graph_interaction_selection_002",
            "graph_zoom",
            "graph_zoom_inspect_surface",
        ),
        (
            "graph_interaction_selection_003",
            "graph_pan",
            "graph_pan_inspect_surface",
        ),
    )


def test_graph_interaction_selection_entry_rejects_execution_path() -> None:
    with pytest.raises(
        ValueError,
        match="execution_path_open must remain false for canonical graph interaction selection entries.",
    ):
        GraphInteractionSelectionEntry(
            selection_entry_id="bad_selection",
            interaction_kind="graph_select",
            selection_scope="scope_a",
            inspect_surface_id="surface_a",
            selection_ready=True,
            inspect_only=True,
            execution_path_open=True,
            operator_visible=True,
            truth_bound=True,
            description="Invalid graph interaction selection entry.",
        )

from __future__ import annotations

import pytest

from MAKSIMAR_CORE_LIB.oob_dashboard.graph_interaction_policy_contract import (
    GraphInteractionPolicyEntry,
    build_graph_interaction_policy_contract,
)


def test_graph_interaction_policy_contract_builds() -> None:
    contract = build_graph_interaction_policy_contract()

    assert contract.contract_id == "graph_interaction_policy_contract_001"
    assert contract.total_entries == 3
    assert contract.allowed_entries == 3
    assert contract.inspect_only_entries == 3
    assert contract.operator_visible_entries == 3
    assert contract.truth_bound_entries == 3


def test_graph_interaction_policy_contract_contains_expected_entries() -> None:
    contract = build_graph_interaction_policy_contract()

    values = tuple(
        (
            entry.policy_entry_id,
            entry.interaction_kind,
            entry.selection_scope,
        )
        for entry in contract.entries
    )

    assert values == (
        (
            "graph_interaction_policy_001",
            "graph_select",
            "dependency_graph_selection",
        ),
        (
            "graph_interaction_policy_002",
            "graph_zoom",
            "dataflow_graph_selection",
        ),
        (
            "graph_interaction_policy_003",
            "graph_pan",
            "combined_graph_inspect_selection",
        ),
    )


def test_graph_interaction_policy_entry_rejects_runtime_mutation() -> None:
    with pytest.raises(
        ValueError,
        match="mutates_runtime must remain false for canonical graph interaction policy entries.",
    ):
        GraphInteractionPolicyEntry(
            policy_entry_id="bad_policy",
            interaction_kind="graph_select",
            selection_scope="scope_a",
            allowed=True,
            inspect_only=True,
            mutates_runtime=True,
            bypasses_control_plane=False,
            operator_visible=True,
            truth_bound=True,
            description="Invalid graph interaction policy entry.",
        )

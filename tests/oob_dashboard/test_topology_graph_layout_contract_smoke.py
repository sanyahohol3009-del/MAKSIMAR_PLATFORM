from __future__ import annotations

import pytest

from MAKSIMAR_CORE_LIB.oob_dashboard.topology_graph_layout_contract import (
    TopologyGraphLayoutEntry,
    build_topology_graph_layout_contract,
)


def test_topology_graph_layout_contract_builds() -> None:
    contract = build_topology_graph_layout_contract()

    assert contract.contract_id == "topology_graph_layout_contract_001"
    assert contract.total_entries == 3
    assert contract.layout_ready_entries == 3
    assert contract.canonical_id_preserved_entries == 3
    assert contract.operator_visible_entries == 3
    assert contract.truth_bound_entries == 3
    assert contract.edge_count == 2


def test_topology_graph_layout_contract_contains_expected_layouts() -> None:
    contract = build_topology_graph_layout_contract()

    values = tuple(
        (
            entry.layout_entry_id,
            entry.canonical_node_id,
            entry.node_projection_id,
            entry.x_slot,
            entry.y_slot,
        )
        for entry in contract.entries
    )

    assert values == (
        (
            "topology_graph_layout_001",
            "mobile_001",
            "mobile_001_graph_projection",
            1,
            0,
        ),
        (
            "topology_graph_layout_002",
            "dev_001",
            "dev_001_graph_projection",
            0,
            1,
        ),
        (
            "topology_graph_layout_003",
            "home_001",
            "home_001_graph_projection",
            2,
            1,
        ),
    )


def test_topology_graph_layout_entry_rejects_negative_slot() -> None:
    with pytest.raises(ValueError, match="x_slot must be >= 0."):
        TopologyGraphLayoutEntry(
            layout_entry_id="bad_layout",
            canonical_node_id="node_a",
            node_projection_id="node_projection_a",
            layout_zone="topology_graph_main_zone",
            x_slot=-1,
            y_slot=0,
            layout_ready=True,
            canonical_id_preserved=True,
            operator_visible=True,
            truth_bound=True,
            description="Invalid layout entry.",
        )

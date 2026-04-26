from __future__ import annotations

import pytest

from MAKSIMAR_CORE_LIB.oob_dashboard.topology_graph_edge_adapter_contract import (
    TopologyGraphEdgeAdapterEntry,
    build_topology_graph_edge_adapter_contract,
)


def test_topology_graph_edge_adapter_contract_builds() -> None:
    contract = build_topology_graph_edge_adapter_contract()

    assert contract.contract_id == "topology_graph_edge_adapter_contract_001"
    assert contract.total_entries == 2
    assert contract.canonical_id_preserved_entries == 2
    assert contract.edge_projection_ready_entries == 2
    assert contract.operator_visible_entries == 2
    assert contract.truth_bound_entries == 2


def test_topology_graph_edge_adapter_contract_contains_expected_edges() -> None:
    contract = build_topology_graph_edge_adapter_contract()

    values = tuple(
        (
            entry.adapter_entry_id,
            entry.source_node_id,
            entry.target_node_id,
            entry.edge_class,
        )
        for entry in contract.entries
    )

    assert values == (
        (
            "topology_graph_edge_adapter_001",
            "dev_001",
            "mobile_001",
            "topology_anchor_edge",
        ),
        (
            "topology_graph_edge_adapter_002",
            "home_001",
            "mobile_001",
            "topology_anchor_edge",
        ),
    )


def test_topology_graph_edge_adapter_entry_rejects_vendor_exposure() -> None:
    with pytest.raises(
        ValueError,
        match="vendor_edge_id_exposed must remain false for canonical topology graph edge adapter entries.",
    ):
        TopologyGraphEdgeAdapterEntry(
            adapter_entry_id="bad_edge_adapter",
            topology_panel_id="panel_node_topology",
            graph_adapter_contract_id="graph_render_adapter_contract_001",
            canonical_edge_id="edge_a",
            source_node_id="node_a",
            target_node_id="node_b",
            edge_class="edge_class_a",
            graph_projection_id="edge_a_projection",
            canonical_id_preserved=True,
            vendor_edge_id_exposed=True,
            edge_projection_ready=True,
            operator_visible=True,
            truth_bound=True,
            description="Invalid edge adapter entry.",
        )

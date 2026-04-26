from __future__ import annotations

import pytest

from MAKSIMAR_CORE_LIB.oob_dashboard.topology_graph_node_adapter_contract import (
    TopologyGraphNodeAdapterEntry,
    build_topology_graph_node_adapter_contract,
)


def test_topology_graph_node_adapter_contract_builds() -> None:
    contract = build_topology_graph_node_adapter_contract()

    assert contract.contract_id == "topology_graph_node_adapter_contract_001"
    assert contract.total_entries == 3
    assert contract.canonical_id_preserved_entries == 3
    assert contract.node_projection_ready_entries == 3
    assert contract.operator_visible_entries == 3
    assert contract.truth_bound_entries == 3


def test_topology_graph_node_adapter_contract_contains_expected_nodes() -> None:
    contract = build_topology_graph_node_adapter_contract()

    values = tuple(
        (
            entry.adapter_entry_id,
            entry.canonical_node_id,
            entry.node_role_type,
            entry.graph_projection_id,
        )
        for entry in contract.entries
    )

    assert values == (
        (
            "topology_graph_node_adapter_001",
            "mobile_001",
            "mobile_node",
            "mobile_001_graph_projection",
        ),
        (
            "topology_graph_node_adapter_002",
            "dev_001",
            "dev_node",
            "dev_001_graph_projection",
        ),
        (
            "topology_graph_node_adapter_003",
            "home_001",
            "home_node",
            "home_001_graph_projection",
        ),
    )


def test_topology_graph_node_adapter_entry_rejects_vendor_exposure() -> None:
    with pytest.raises(
        ValueError,
        match="vendor_node_id_exposed must remain false for canonical topology graph node adapter entries.",
    ):
        TopologyGraphNodeAdapterEntry(
            adapter_entry_id="bad_node_adapter",
            topology_panel_id="panel_node_topology",
            graph_adapter_contract_id="graph_render_adapter_contract_001",
            canonical_node_id="node_a",
            node_role_type="node_role",
            graph_projection_id="node_a_projection",
            canonical_id_preserved=True,
            vendor_node_id_exposed=True,
            node_projection_ready=True,
            operator_visible=True,
            truth_bound=True,
            description="Invalid node adapter entry.",
        )

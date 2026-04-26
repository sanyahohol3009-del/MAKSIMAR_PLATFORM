from __future__ import annotations

import pytest

from MAKSIMAR_CORE_LIB.oob_dashboard.dataflow_graph_adapter_contract import (
    DataflowGraphAdapterEntry,
    build_dataflow_graph_adapter_contract,
)


def test_dataflow_graph_adapter_contract_builds() -> None:
    contract = build_dataflow_graph_adapter_contract()

    assert contract.contract_id == "dataflow_graph_adapter_contract_001"
    assert contract.total_entries == 5
    assert contract.canonical_id_preserved_entries == 5
    assert contract.flow_projection_ready_entries == 5
    assert contract.operator_visible_entries == 5
    assert contract.truth_bound_entries == 5


def test_dataflow_graph_adapter_contract_contains_expected_entries() -> None:
    contract = build_dataflow_graph_adapter_contract()

    values = tuple(
        (
            entry.adapter_entry_id,
            entry.source_component,
            entry.target_component,
            entry.flow_class,
        )
        for entry in contract.entries
    )

    assert values == (
        (
            "dataflow_graph_adapter_001",
            "control_plane",
            "execution_control",
            "control_to_execution",
        ),
        (
            "dataflow_graph_adapter_002",
            "execution_control",
            "workers",
            "execution_to_workers",
        ),
        (
            "dataflow_graph_adapter_003",
            "workers",
            "data_plane",
            "workers_to_data_plane",
        ),
        (
            "dataflow_graph_adapter_004",
            "execution_observability",
            "oob_dashboard",
            "observability_projection",
        ),
        (
            "dataflow_graph_adapter_005",
            "control_plane",
            "execution_observability",
            "control_to_observability",
        ),
    )


def test_dataflow_graph_adapter_entry_rejects_vendor_exposure() -> None:
    with pytest.raises(
        ValueError,
        match="vendor_flow_id_exposed must remain false for canonical dataflow graph adapter entries.",
    ):
        DataflowGraphAdapterEntry(
            adapter_entry_id="bad_dataflow_adapter",
            dataflow_panel_id="panel_data_flow",
            graph_adapter_contract_id="graph_render_adapter_contract_001",
            canonical_flow_id="flow_a",
            source_component="source_a",
            target_component="target_b",
            flow_class="flow_class_a",
            graph_projection_id="flow_projection_a",
            canonical_id_preserved=True,
            vendor_flow_id_exposed=True,
            flow_projection_ready=True,
            operator_visible=True,
            truth_bound=True,
            description="Invalid dataflow graph adapter entry.",
        )

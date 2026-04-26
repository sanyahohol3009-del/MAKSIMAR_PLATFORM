from __future__ import annotations

import pytest

from MAKSIMAR_CORE_LIB.oob_dashboard.graph_render_adapter_contract import (
    GraphRenderAdapterEntry,
    build_graph_render_adapter_contract,
)


def test_graph_render_adapter_contract_builds() -> None:
    contract = build_graph_render_adapter_contract()

    assert contract.contract_id == "graph_render_adapter_contract_001"
    assert contract.total_entries == 3
    assert contract.canonical_id_preserved_entries == 3
    assert contract.replaceable_entries == 3
    assert contract.operator_visible_entries == 3
    assert contract.truth_bound_entries == 3


def test_graph_render_adapter_contract_contains_expected_targets() -> None:
    contract = build_graph_render_adapter_contract()

    values = tuple(
        (entry.adapter_entry_id, entry.adapter_target, entry.backend_id)
        for entry in contract.entries
    )

    assert values == (
        (
            "graph_render_adapter_001",
            "topology_family_graph_projection",
            "visual_backend_graph_001",
        ),
        (
            "graph_render_adapter_002",
            "dependency_dataflow_graph_projection",
            "visual_backend_graph_001",
        ),
        (
            "graph_render_adapter_003",
            "module_graph_projection",
            "visual_backend_graph_001",
        ),
    )


def test_graph_render_adapter_entry_rejects_vendor_leakage() -> None:
    with pytest.raises(
        ValueError,
        match="vendor_id_exposed must remain false for canonical graph render adapter entries.",
    ):
        GraphRenderAdapterEntry(
            adapter_entry_id="bad_graph_adapter",
            backend_id="visual_backend_graph_001",
            adapter_target="bad_target",
            adapter_mode="canonical_to_graph_backend",
            canonical_id_preserved=True,
            vendor_id_exposed=True,
            truth_leakage_allowed=False,
            replaceable=True,
            operator_visible=True,
            truth_bound=True,
            description="Invalid graph adapter entry.",
        )

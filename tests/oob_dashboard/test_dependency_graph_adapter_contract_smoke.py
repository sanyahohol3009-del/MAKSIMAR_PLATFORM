from __future__ import annotations

import pytest

from MAKSIMAR_CORE_LIB.oob_dashboard.dependency_graph_adapter_contract import (
    DependencyGraphAdapterEntry,
    build_dependency_graph_adapter_contract,
)


def test_dependency_graph_adapter_contract_builds() -> None:
    contract = build_dependency_graph_adapter_contract()

    assert contract.contract_id == "dependency_graph_adapter_contract_001"
    assert contract.total_entries == 3
    assert contract.canonical_id_preserved_entries == 3
    assert contract.dependency_projection_ready_entries == 3
    assert contract.operator_visible_entries == 3
    assert contract.truth_bound_entries == 3


def test_dependency_graph_adapter_contract_contains_expected_entries() -> None:
    contract = build_dependency_graph_adapter_contract()

    values = tuple(
        (
            entry.adapter_entry_id,
            entry.upstream_module_id,
            entry.downstream_module_id,
            entry.dependency_kind,
        )
        for entry in contract.entries
    )

    assert values == (
        (
            "dependency_graph_adapter_001",
            "control_plane",
            "execution_control",
            "execution_dependency",
        ),
        (
            "dependency_graph_adapter_002",
            "execution_control",
            "execution_observability",
            "execution_dependency",
        ),
        (
            "dependency_graph_adapter_003",
            "execution_observability",
            "oob_dashboard",
            "projection_dependency",
        ),
    )


def test_dependency_graph_adapter_entry_rejects_vendor_exposure() -> None:
    with pytest.raises(
        ValueError,
        match="vendor_dependency_id_exposed must remain false for canonical dependency graph adapter entries.",
    ):
        DependencyGraphAdapterEntry(
            adapter_entry_id="bad_dependency_adapter",
            dependency_panel_id="panel_dependency_map",
            graph_adapter_contract_id="graph_render_adapter_contract_001",
            canonical_dependency_id="dep_a",
            upstream_module_id="module_a",
            downstream_module_id="module_b",
            dependency_kind="dependency_kind",
            graph_projection_id="dep_a_projection",
            canonical_id_preserved=True,
            vendor_dependency_id_exposed=True,
            dependency_projection_ready=True,
            operator_visible=True,
            truth_bound=True,
            description="Invalid dependency graph adapter entry.",
        )

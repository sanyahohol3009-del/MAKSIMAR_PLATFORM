from __future__ import annotations

import pytest

from MAKSIMAR_CORE_LIB.oob_dashboard.module_graph_surface_adapter_contract import (
    ModuleGraphSurfaceAdapterEntry,
    build_module_graph_surface_adapter_contract,
)


def test_module_graph_surface_adapter_contract_builds() -> None:
    contract = build_module_graph_surface_adapter_contract()

    assert contract.contract_id == "module_graph_surface_adapter_contract_001"
    assert contract.total_entries == 3
    assert contract.canonical_id_preserved_entries == 3
    assert contract.surface_projection_ready_entries == 3
    assert contract.operator_visible_entries == 3
    assert contract.truth_bound_entries == 3


def test_module_graph_surface_adapter_contract_contains_expected_modules() -> None:
    contract = build_module_graph_surface_adapter_contract()

    values = tuple(
        (
            entry.adapter_entry_id,
            entry.module_id,
            entry.surface_id,
            entry.workspace_id,
        )
        for entry in contract.entries
    )

    assert values == (
        (
            "module_graph_surface_adapter_001",
            "module_manifest_001",
            "foundation_monitoring_module_surface",
            "workspace_foundation_monitoring",
        ),
        (
            "module_graph_surface_adapter_002",
            "module_manifest_002",
            "operator_interaction_module_surface",
            "workspace_operator_interaction",
        ),
        (
            "module_graph_surface_adapter_003",
            "module_manifest_003",
            "optional_product_module_surface",
            "workspace_operator_interaction",
        ),
    )


def test_module_graph_surface_adapter_entry_rejects_vendor_exposure() -> None:
    with pytest.raises(
        ValueError,
        match="vendor_surface_id_exposed must remain false for canonical module graph surface adapter entries.",
    ):
        ModuleGraphSurfaceAdapterEntry(
            adapter_entry_id="bad_surface_adapter",
            module_id="module_manifest_001",
            surface_id="surface_a",
            workspace_id="workspace_a",
            graph_adapter_contract_id="graph_render_adapter_contract_001",
            graph_projection_id="surface_projection_a",
            canonical_id_preserved=True,
            vendor_surface_id_exposed=True,
            surface_projection_ready=True,
            operator_visible=True,
            truth_bound=True,
            description="Invalid module graph surface adapter entry.",
        )

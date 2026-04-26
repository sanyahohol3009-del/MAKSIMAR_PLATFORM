from __future__ import annotations

import pytest

from MAKSIMAR_CORE_LIB.oob_dashboard.module_graph_audit_adapter_contract import (
    ModuleGraphAuditAdapterEntry,
    build_module_graph_audit_adapter_contract,
)


def test_module_graph_audit_adapter_contract_builds() -> None:
    contract = build_module_graph_audit_adapter_contract()

    assert contract.contract_id == "module_graph_audit_adapter_contract_001"
    assert contract.total_entries == 3
    assert contract.canonical_id_preserved_entries == 3
    assert contract.audit_projection_ready_entries == 3
    assert contract.operator_visible_entries == 3
    assert contract.truth_bound_entries == 3


def test_module_graph_audit_adapter_contract_contains_expected_modules() -> None:
    contract = build_module_graph_audit_adapter_contract()

    values = tuple(
        (
            entry.adapter_entry_id,
            entry.module_id,
            entry.registry_audit_id,
            entry.graph_projection_id,
        )
        for entry in contract.entries
    )

    assert values == (
        (
            "module_graph_audit_adapter_001",
            "module_manifest_001",
            "module_registry_audit_001",
            "module_manifest_001_audit_graph_projection",
        ),
        (
            "module_graph_audit_adapter_002",
            "module_manifest_002",
            "module_registry_audit_002",
            "module_manifest_002_audit_graph_projection",
        ),
        (
            "module_graph_audit_adapter_003",
            "module_manifest_003",
            "module_registry_audit_003",
            "module_manifest_003_audit_graph_projection",
        ),
    )


def test_module_graph_audit_adapter_entry_rejects_vendor_exposure() -> None:
    with pytest.raises(
        ValueError,
        match="vendor_audit_id_exposed must remain false for canonical module graph audit adapter entries.",
    ):
        ModuleGraphAuditAdapterEntry(
            adapter_entry_id="bad_audit_adapter",
            module_id="module_manifest_001",
            registry_audit_id="audit_a",
            graph_adapter_contract_id="graph_render_adapter_contract_001",
            graph_projection_id="audit_projection_a",
            audit_visible=True,
            canonical_id_preserved=True,
            vendor_audit_id_exposed=True,
            audit_projection_ready=True,
            operator_visible=True,
            truth_bound=True,
            description="Invalid module graph audit adapter entry.",
        )

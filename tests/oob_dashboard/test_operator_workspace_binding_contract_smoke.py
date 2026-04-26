from __future__ import annotations

from MAKSIMAR_CORE_LIB.oob_dashboard.operator_workspace_binding_contract import (
    build_operator_workspace_binding_contract,
)


def test_operator_workspace_binding_contract_builds() -> None:
    contract = build_operator_workspace_binding_contract()

    assert len(contract.entries) == 2
    assert contract.entries[0].dashboard_id == "main_operator_dashboard"


def test_operator_workspace_binding_contract_values() -> None:
    contract = build_operator_workspace_binding_contract()
    entry_map = {entry.workspace_id: entry for entry in contract.entries}

    primary_entry = entry_map["workspace_operator_interaction"]
    assert primary_entry.binding_role == "primary_operator_workspace"
    assert primary_entry.workspace_order == 0
    assert primary_entry.is_primary_workspace is True
    assert primary_entry.read_only_binding is True

    secondary_entry = entry_map["workspace_foundation_monitoring"]
    assert secondary_entry.binding_role == "secondary_foundation_workspace"
    assert secondary_entry.workspace_order == 1
    assert secondary_entry.is_primary_workspace is False
    assert secondary_entry.read_only_binding is True

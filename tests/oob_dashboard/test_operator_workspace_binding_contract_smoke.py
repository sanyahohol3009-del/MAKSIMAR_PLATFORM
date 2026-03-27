from __future__ import annotations

from MAKSIMAR_CORE_LIB.oob_dashboard import (
    build_operator_workspace_binding_contract,
)


def test_operator_workspace_binding_contract_builds() -> None:
    """Operator workspace binding contract should build successfully."""
    contract = build_operator_workspace_binding_contract()

    assert contract.total_entries == 1
    assert contract.primary_operator_workspace_entries == 1
    assert contract.interactive_entries == 1
    assert contract.read_only_entries == 0


def test_operator_workspace_binding_entry() -> None:
    """Operator workspace binding entry should remain canonical."""
    contract = build_operator_workspace_binding_contract()
    entry = contract.entries[0]

    assert entry.dashboard_id == "dashboard_main_operator_001"
    assert entry.workspace_id == "workspace_operator_main"
    assert entry.workspace_role == "operator_surface"
    assert entry.display_target_id == "display_primary_operator"
    assert entry.is_primary_operator_workspace is True
    assert entry.supports_interaction is True
    assert entry.read_only is False

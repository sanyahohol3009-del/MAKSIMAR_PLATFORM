from __future__ import annotations

from MAKSIMAR_CORE_LIB.oob_dashboard.workspace_registry_contract import (
    build_workspace_registry_contract,
)


def test_workspace_registry_contract_builds() -> None:
    contract = build_workspace_registry_contract()

    assert len(contract.entries) == 2
    assert contract.entries[0].workspace_id == "workspace_foundation_monitoring"
    assert contract.entries[1].workspace_id == "workspace_operator_interaction"


def test_workspace_registry_foundation_entry() -> None:
    contract = build_workspace_registry_contract()
    workspace_map = {entry.workspace_id: entry for entry in contract.entries}

    foundation_entry = workspace_map["workspace_foundation_monitoring"]
    assert foundation_entry.workspace_role == "foundation_monitoring"
    assert foundation_entry.primary_display_target_id == "display_foundation_primary"
    assert foundation_entry.included_panel_ids == (
        "system_status",
        "guard_chain",
        "incidents",
        "logs",
        "topology",
    )


def test_workspace_registry_operator_entry() -> None:
    contract = build_workspace_registry_contract()
    workspace_map = {entry.workspace_id: entry for entry in contract.entries}

    operator_entry = workspace_map["workspace_operator_interaction"]
    assert operator_entry.workspace_role == "operator_interaction"
    assert operator_entry.primary_display_target_id == "display_operator_interaction"
    assert operator_entry.included_panel_ids == (
        "action_queue",
        "approval_queue",
        "audit_timeline",
    )

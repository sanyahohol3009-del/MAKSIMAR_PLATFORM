from __future__ import annotations

from MAKSIMAR_CORE_LIB.oob_dashboard.panel_role_contract import (
    build_panel_role_contract,
)


def test_panel_role_contract_builds() -> None:
    contract = build_panel_role_contract()

    assert len(contract.entries) == 8
    assert contract.entries[0].panel_id == "system_status"
    assert contract.entries[-1].panel_id == "audit_timeline"


def test_panel_role_contract_values() -> None:
    contract = build_panel_role_contract()
    role_map = {entry.panel_id: entry for entry in contract.entries}

    assert role_map["system_status"].panel_role == "read_only_monitoring"
    assert role_map["action_queue"].panel_role == "operator_interaction"

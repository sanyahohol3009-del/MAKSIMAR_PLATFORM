from __future__ import annotations

from MAKSIMAR_CORE_LIB.oob_dashboard.panel_family_contract import (
    build_panel_family_contract,
)


def test_panel_family_contract_builds() -> None:
    contract = build_panel_family_contract()

    assert len(contract.entries) == 8
    assert contract.entries[0].panel_id == "system_status"
    assert contract.entries[-1].panel_id == "audit_timeline"


def test_panel_family_contract_values() -> None:
    contract = build_panel_family_contract()
    family_map = {entry.panel_id: entry for entry in contract.entries}

    assert family_map["system_status"].panel_family == "foundation"
    assert family_map["action_queue"].panel_family == "interaction"

from __future__ import annotations

from MAKSIMAR_CORE_LIB.oob_dashboard.panel_kind_contract import (
    build_panel_kind_contract,
)


def test_panel_kind_contract_builds() -> None:
    contract = build_panel_kind_contract()

    assert len(contract.entries) == 8
    assert contract.entries[0].panel_id == "system_status"
    assert contract.entries[-1].panel_id == "audit_timeline"


def test_panel_kind_contract_values() -> None:
    contract = build_panel_kind_contract()
    kind_map = {entry.panel_id: entry for entry in contract.entries}

    assert kind_map["system_status"].panel_kind == "status"
    assert kind_map["logs"].panel_kind == "log"
    assert kind_map["audit_timeline"].panel_kind == "audit"

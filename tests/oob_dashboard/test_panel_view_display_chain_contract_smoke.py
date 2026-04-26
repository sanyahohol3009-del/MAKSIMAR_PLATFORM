from __future__ import annotations

from MAKSIMAR_CORE_LIB.oob_dashboard.panel_view_display_chain_contract import (
    build_panel_view_display_chain_contract,
)


def test_panel_view_display_chain_contract_builds() -> None:
    contract = build_panel_view_display_chain_contract()

    assert len(contract.entries) == 8
    assert contract.entries[0].panel_id == "system_status"
    assert contract.entries[-1].panel_id == "audit_timeline"


def test_panel_view_display_chain_foundation_entries() -> None:
    contract = build_panel_view_display_chain_contract()
    chain_map = {entry.panel_id: entry for entry in contract.entries}

    assert chain_map["system_status"].view_id == "view_foundation_status"
    assert chain_map["system_status"].display_target_id == "display_foundation_primary"
    assert chain_map["system_status"].display_role == "foundation_primary_display"

    assert chain_map["logs"].view_id == "view_foundation_observability"
    assert chain_map["logs"].display_target_id == "display_foundation_secondary"
    assert chain_map["logs"].display_zone == "foundation_secondary_zone"


def test_panel_view_display_chain_interaction_entries() -> None:
    contract = build_panel_view_display_chain_contract()
    chain_map = {entry.panel_id: entry for entry in contract.entries}

    assert chain_map["action_queue"].view_id == "view_operator_interaction"
    assert chain_map["action_queue"].display_target_id == "display_operator_interaction"
    assert chain_map["action_queue"].display_role == "operator_interaction_display"

    assert chain_map["audit_timeline"].display_zone == "operator_interaction_zone"


def test_panel_view_display_chain_entries_are_default() -> None:
    contract = build_panel_view_display_chain_contract()

    for entry in contract.entries:
        assert entry.is_default_chain is True
        assert entry.description

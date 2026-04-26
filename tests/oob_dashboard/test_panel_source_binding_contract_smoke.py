from __future__ import annotations

from MAKSIMAR_CORE_LIB.oob_dashboard.panel_source_binding_contract import (
    build_panel_source_binding_contract,
)


def test_panel_source_binding_contract_builds() -> None:
    contract = build_panel_source_binding_contract()

    assert len(contract.entries) == 8
    assert contract.entries[0].panel_id == "system_status"
    assert contract.entries[-1].panel_id == "audit_timeline"


def test_panel_source_binding_foundation_entries() -> None:
    contract = build_panel_source_binding_contract()
    binding_map = {entry.panel_id: entry for entry in contract.entries}

    assert binding_map["system_status"].source_contract_name == (
        "system_status_panel_content_contract"
    )
    assert binding_map["guard_chain"].source_contract_name == (
        "guard_chain_panel_content_contract"
    )
    assert binding_map["topology"].source_contract_name == (
        "topology_panel_content_contract"
    )


def test_panel_source_binding_interaction_entries() -> None:
    contract = build_panel_source_binding_contract()
    binding_map = {entry.panel_id: entry for entry in contract.entries}

    assert binding_map["action_queue"].source_scope == "interaction"
    assert binding_map["approval_queue"].source_scope == "interaction"
    assert binding_map["audit_timeline"].source_scope == "interaction"


def test_panel_source_binding_all_entries_are_read_only() -> None:
    contract = build_panel_source_binding_contract()

    for entry in contract.entries:
        assert entry.read_only is True
        assert entry.description

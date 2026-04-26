from __future__ import annotations

from MAKSIMAR_CORE_LIB.oob_dashboard.panel_content_contract import (
    build_panel_content_contract,
)


def test_panel_content_contract_builds() -> None:
    contract = build_panel_content_contract()

    assert len(contract.entries) == 8
    assert contract.entries[0].panel_id == "system_status"
    assert contract.entries[-1].panel_id == "audit_timeline"


def test_panel_content_foundation_entries() -> None:
    contract = build_panel_content_contract()
    content_map = {entry.panel_id: entry for entry in contract.entries}

    assert content_map["system_status"].content_contract_name == (
        "system_status_panel_content_contract"
    )
    assert content_map["logs"].content_kind == "log_tail"
    assert content_map["topology"].content_scope == "foundation"


def test_panel_content_interaction_entries() -> None:
    contract = build_panel_content_contract()
    content_map = {entry.panel_id: entry for entry in contract.entries}

    assert content_map["action_queue"].content_kind == "queue"
    assert content_map["approval_queue"].content_scope == "interaction"
    assert content_map["audit_timeline"].content_kind == "timeline"


def test_panel_content_entries_are_read_only() -> None:
    contract = build_panel_content_contract()

    for entry in contract.entries:
        assert entry.read_only is True
        assert entry.description

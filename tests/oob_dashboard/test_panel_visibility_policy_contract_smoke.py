from __future__ import annotations

from MAKSIMAR_CORE_LIB.oob_dashboard.panel_visibility_policy_contract import (
    build_panel_visibility_policy_contract,
)


def test_panel_visibility_policy_contract_builds() -> None:
    contract = build_panel_visibility_policy_contract()

    assert len(contract.entries) == 8
    assert contract.entries[0].panel_id == "system_status"
    assert contract.entries[-1].panel_id == "audit_timeline"


def test_panel_visibility_policy_foundation_entries() -> None:
    contract = build_panel_visibility_policy_contract()
    visibility_map = {entry.panel_id: entry for entry in contract.entries}

    assert visibility_map["system_status"].visibility_policy == "always_visible"
    assert visibility_map["system_status"].visible_in_oob_dashboard is True
    assert visibility_map["system_status"].visible_in_main_dashboard is True

    assert visibility_map["guard_chain"].visible_in_navigation is True
    assert visibility_map["incidents"].operator_visible is True


def test_panel_visibility_policy_interaction_entries() -> None:
    contract = build_panel_visibility_policy_contract()
    visibility_map = {entry.panel_id: entry for entry in contract.entries}

    assert visibility_map["action_queue"].visibility_policy == "policy_visible"
    assert visibility_map["approval_queue"].visibility_policy == "policy_visible"
    assert visibility_map["audit_timeline"].visibility_policy == "policy_visible"


def test_panel_visibility_policy_entries_have_descriptions() -> None:
    contract = build_panel_visibility_policy_contract()

    for entry in contract.entries:
        assert entry.description

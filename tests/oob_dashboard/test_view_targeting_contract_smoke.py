from __future__ import annotations

from MAKSIMAR_CORE_LIB.oob_dashboard.view_targeting_contract import (
    build_view_targeting_contract,
    resolve_view_scope,
    resolve_view_target_kind,
)


def test_view_targeting_contract_builds() -> None:
    contract = build_view_targeting_contract()

    assert len(contract.entries) == 8
    assert contract.entries[0].panel_id == "system_status"
    assert contract.entries[-1].panel_id == "audit_timeline"


def test_view_targeting_contract_assigns_foundation_views() -> None:
    contract = build_view_targeting_contract()
    targeting_map = {entry.panel_id: entry for entry in contract.entries}

    assert targeting_map["system_status"].view_id == "view_foundation_status"
    assert targeting_map["logs"].view_id == "view_foundation_observability"


def test_view_targeting_contract_assigns_interaction_views() -> None:
    contract = build_view_targeting_contract()
    targeting_map = {entry.panel_id: entry for entry in contract.entries}

    assert targeting_map["action_queue"].view_id == "view_operator_interaction"
    assert targeting_map["approval_queue"].view_id == "view_operator_interaction"
    assert targeting_map["audit_timeline"].view_id == "view_operator_interaction"


def test_resolve_view_target_kind_smoke() -> None:
    assert resolve_view_target_kind("system_status") == "foundation_view"
    assert resolve_view_target_kind("audit_timeline") == "interaction_view"


def test_resolve_view_scope_smoke() -> None:
    assert resolve_view_scope("system_status") == "foundation"
    assert resolve_view_scope("audit_timeline") == "interaction"

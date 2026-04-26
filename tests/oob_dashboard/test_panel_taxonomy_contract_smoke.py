from __future__ import annotations

from MAKSIMAR_CORE_LIB.oob_dashboard.panel_taxonomy_contract import (
    build_panel_taxonomy_contract,
    resolve_panel_role,
)


def test_panel_taxonomy_contract_builds() -> None:
    contract = build_panel_taxonomy_contract()

    assert len(contract.entries) == 8
    assert contract.entries[0].panel_id == "system_status"
    assert contract.entries[-1].panel_id == "audit_timeline"


def test_panel_taxonomy_foundation_entries() -> None:
    contract = build_panel_taxonomy_contract()
    taxonomy_map = {entry.panel_id: entry for entry in contract.entries}

    assert taxonomy_map["system_status"].panel_family == "foundation"
    assert taxonomy_map["system_status"].panel_kind == "status"
    assert taxonomy_map["system_status"].panel_role == "read_only_monitoring"

    assert taxonomy_map["logs"].panel_kind == "log"
    assert taxonomy_map["topology"].panel_kind == "topology"


def test_panel_taxonomy_interaction_entries() -> None:
    contract = build_panel_taxonomy_contract()
    taxonomy_map = {entry.panel_id: entry for entry in contract.entries}

    assert taxonomy_map["action_queue"].panel_family == "interaction"
    assert taxonomy_map["action_queue"].panel_kind == "queue"
    assert taxonomy_map["action_queue"].panel_role == "operator_interaction"

    assert taxonomy_map["audit_timeline"].panel_kind == "audit"


def test_resolve_panel_role_smoke() -> None:
    assert resolve_panel_role("system_status") == "read_only_monitoring"
    assert resolve_panel_role("action_queue") == "operator_interaction"

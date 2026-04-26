from __future__ import annotations

from MAKSIMAR_CORE_LIB.oob_dashboard.panel_binding_contract import (
    build_panel_binding_contract,
    resolve_binding_reason,
    resolve_display_target_id,
)


def test_panel_binding_contract_builds() -> None:
    contract = build_panel_binding_contract()

    assert len(contract.entries) == 8
    assert contract.entries[0].panel_id == "system_status"
    assert contract.entries[-1].panel_id == "audit_timeline"


def test_panel_binding_contract_assigns_foundation_panels() -> None:
    contract = build_panel_binding_contract()
    binding_map = {entry.panel_id: entry for entry in contract.entries}

    assert binding_map["system_status"].display_target_id == "display_foundation_primary"
    assert binding_map["logs"].display_target_id == "display_foundation_secondary"


def test_panel_binding_contract_assigns_interaction_panels() -> None:
    contract = build_panel_binding_contract()
    binding_map = {entry.panel_id: entry for entry in contract.entries}

    assert binding_map["action_queue"].display_target_id == "display_operator_interaction"
    assert binding_map["approval_queue"].display_target_id == "display_operator_interaction"
    assert binding_map["audit_timeline"].display_target_id == "display_operator_interaction"


def test_resolve_display_target_id_smoke() -> None:
    assert resolve_display_target_id("system_status") == "display_foundation_primary"
    assert resolve_display_target_id("logs") == "display_foundation_secondary"
    assert resolve_display_target_id("audit_timeline") == "display_operator_interaction"


def test_resolve_binding_reason_smoke() -> None:
    assert resolve_binding_reason("system_status") == "foundation_visibility"
    assert resolve_binding_reason("action_queue") == "operator_interaction_visibility"

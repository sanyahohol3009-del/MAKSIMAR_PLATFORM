from __future__ import annotations

from MAKSIMAR_CORE_LIB.oob_dashboard.operator_audit_visibility_contract import (
    build_operator_audit_visibility_contract,
)


def test_operator_audit_visibility_contract_builds() -> None:
    contract = build_operator_audit_visibility_contract()

    assert len(contract.entries) == 1
    assert contract.entries[0].dashboard_id == "main_operator_dashboard"


def test_operator_audit_visibility_contract_values() -> None:
    contract = build_operator_audit_visibility_contract()
    entry = contract.entries[0]

    assert entry.audit_surface_id == "audit_timeline_surface"
    assert entry.audit_scope == "operator_action_audit"
    assert entry.audit_visibility_mode == "always_visible_audit_path"
    assert entry.hidden_audit_allowed is False
    assert entry.policy_visibility_required is True
    assert entry.approval_visibility_required is True

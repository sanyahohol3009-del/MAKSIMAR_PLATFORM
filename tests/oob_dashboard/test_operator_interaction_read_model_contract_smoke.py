from __future__ import annotations

from MAKSIMAR_CORE_LIB.oob_dashboard.operator_interaction_read_model_contract import (
    build_operator_interaction_read_model_contract,
    normalize_dashboard_id,
)


def test_operator_interaction_read_model_contract_builds() -> None:
    contract = build_operator_interaction_read_model_contract()

    assert contract.total_entries >= 1
    assert len(contract.entries) == contract.total_entries


def test_operator_interaction_read_model_contract_has_operator_visible_entries() -> None:
    contract = build_operator_interaction_read_model_contract()

    assert contract.operator_visible_entries == contract.total_entries
    assert all(entry.operator_visible for entry in contract.entries)


def test_operator_interaction_read_model_contract_preserves_approval_semantics() -> None:
    contract = build_operator_interaction_read_model_contract()

    for entry in contract.entries:
        if entry.approval_required:
            assert entry.interaction_lane == "approval_bound_lane"
            assert entry.interaction_surface_state == "approval_bound_interaction_surface"
            assert entry.approval_state == "approval_required"
        else:
            assert entry.interaction_lane == "read_only_lane"
            assert entry.interaction_surface_state == "read_only_interaction_surface"
            assert entry.approval_state == "approval_not_required"


def test_operator_interaction_read_model_contract_exposes_audit_visibility() -> None:
    contract = build_operator_interaction_read_model_contract()

    for entry in contract.entries:
        assert entry.audit_visibility_state == "audit_visible_with_policy_and_approval"
        assert entry.handoff_state == "handoff_ready"
        assert entry.handoff_ready is True


def test_normalize_dashboard_id_supports_legacy_and_canonical() -> None:
    assert normalize_dashboard_id("dashboard_main_operator_001") == "main_operator_dashboard"
    assert normalize_dashboard_id("main_operator_dashboard") == "main_operator_dashboard"

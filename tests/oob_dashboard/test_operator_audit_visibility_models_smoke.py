from __future__ import annotations

import pytest

from MAKSIMAR_CORE_LIB.oob_dashboard.operator_audit_visibility_models import (
    OperatorAuditVisibilityContract,
    OperatorAuditVisibilityEntry,
)


def test_operator_audit_visibility_entry_smoke() -> None:
    entry = OperatorAuditVisibilityEntry(
        dashboard_id="main_operator_dashboard",
        audit_surface_id="audit_timeline_surface",
        audit_scope="operator_action_audit",
        audit_visibility_mode="always_visible_audit_path",
        hidden_audit_allowed=False,
        policy_visibility_required=True,
        approval_visibility_required=True,
        description="Audit visibility description.",
    )

    assert entry.dashboard_id == "main_operator_dashboard"


def test_operator_audit_visibility_entry_rejects_hidden_audit() -> None:
    with pytest.raises(ValueError, match="hidden_audit_allowed must be False"):
        OperatorAuditVisibilityEntry(
            dashboard_id="main_operator_dashboard",
            audit_surface_id="audit_timeline_surface",
            audit_scope="operator_action_audit",
            audit_visibility_mode="always_visible_audit_path",
            hidden_audit_allowed=True,
            policy_visibility_required=True,
            approval_visibility_required=True,
            description="Audit visibility description.",
        )


def test_operator_audit_visibility_contract_rejects_duplicates() -> None:
    entry_a = OperatorAuditVisibilityEntry(
        dashboard_id="main_operator_dashboard",
        audit_surface_id="audit_timeline_surface",
        audit_scope="operator_action_audit",
        audit_visibility_mode="always_visible_audit_path",
        hidden_audit_allowed=False,
        policy_visibility_required=True,
        approval_visibility_required=True,
        description="A",
    )
    entry_b = OperatorAuditVisibilityEntry(
        dashboard_id="main_operator_dashboard",
        audit_surface_id="audit_timeline_surface",
        audit_scope="operator_action_audit",
        audit_visibility_mode="always_visible_audit_path",
        hidden_audit_allowed=False,
        policy_visibility_required=True,
        approval_visibility_required=True,
        description="B",
    )

    with pytest.raises(ValueError, match="duplicate dashboard_id detected"):
        OperatorAuditVisibilityContract(entries=(entry_a, entry_b))

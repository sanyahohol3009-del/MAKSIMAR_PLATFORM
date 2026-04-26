from __future__ import annotations

import pytest

from MAKSIMAR_CORE_LIB.oob_dashboard.owner_review_package_models import (
    OwnerReviewPackageContract,
    OwnerReviewPackageEntry,
)


def test_owner_review_package_entry_builds() -> None:
    """Owner review package entry should build successfully."""
    entry = OwnerReviewPackageEntry(
        owner_review_package_id="owner_review_package_001",
        operator_intent_id="operator_intent_001",
        panel_id="action_queue",
        workspace_id="workspace_operator_main",
        owner_review_package_state="owner_review_package_ready",
        owner_review_package_class="read_only_review_package",
        owner_review_evidence_mode="preview_and_audit_evidence",
        approval_required=False,
        handoff_ready=True,
        audit_visible=True,
        operator_visible=True,
        trace_id="trace_operator_intent_001",
        description="Canonical owner review package entry.",
    )

    assert entry.owner_review_package_id == "owner_review_package_001"
    assert entry.owner_review_package_state == "owner_review_package_ready"
    assert entry.owner_review_package_class == "read_only_review_package"


def test_owner_review_package_entry_rejects_non_audit_visible() -> None:
    """Owner review package entry must remain audit-visible."""
    with pytest.raises(
        ValueError,
        match="audit_visible must remain true for canonical owner review packages.",
    ):
        OwnerReviewPackageEntry(
            owner_review_package_id="owner_review_package_invalid",
            operator_intent_id="operator_intent_001",
            panel_id="action_queue",
            workspace_id="workspace_operator_main",
            owner_review_package_state="owner_review_package_ready",
            owner_review_package_class="read_only_review_package",
            owner_review_evidence_mode="preview_and_audit_evidence",
            approval_required=False,
            handoff_ready=True,
            audit_visible=False,
            operator_visible=True,
            trace_id="trace_operator_intent_001",
            description="Invalid owner review package entry.",
        )


def test_owner_review_package_contract_builds() -> None:
    """Owner review package contract should build successfully."""
    entries = (
        OwnerReviewPackageEntry(
            owner_review_package_id="owner_review_package_001",
            operator_intent_id="operator_intent_001",
            panel_id="action_queue",
            workspace_id="workspace_operator_main",
            owner_review_package_state="owner_review_package_ready",
            owner_review_package_class="read_only_review_package",
            owner_review_evidence_mode="preview_and_audit_evidence",
            approval_required=False,
            handoff_ready=True,
            audit_visible=True,
            operator_visible=True,
            trace_id="trace_operator_intent_001",
            description="Read-only review package entry.",
        ),
        OwnerReviewPackageEntry(
            owner_review_package_id="owner_review_package_002",
            operator_intent_id="operator_intent_003",
            panel_id="approval_queue",
            workspace_id="workspace_operator_main",
            owner_review_package_state="owner_review_package_ready",
            owner_review_package_class="approval_bound_review_package",
            owner_review_evidence_mode="preview_approval_and_audit_evidence",
            approval_required=True,
            handoff_ready=True,
            audit_visible=True,
            operator_visible=True,
            trace_id="trace_operator_intent_003",
            description="Approval-bound review package entry.",
        ),
    )

    contract = OwnerReviewPackageContract(
        contract_id="owner_review_package_contract_001",
        total_entries=2,
        read_only_review_entries=1,
        approval_bound_review_entries=1,
        audit_visible_entries=2,
        operator_visible_entries=2,
        entries=entries,
    )

    assert contract.total_entries == 2
    assert contract.read_only_review_entries == 1
    assert contract.approval_bound_review_entries == 1

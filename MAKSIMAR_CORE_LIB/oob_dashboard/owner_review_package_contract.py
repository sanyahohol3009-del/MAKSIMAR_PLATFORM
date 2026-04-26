from __future__ import annotations

from MAKSIMAR_CORE_LIB.oob_dashboard.action_queue_panel_content_contract import (
    build_action_queue_panel_content_contract,
)
from MAKSIMAR_CORE_LIB.oob_dashboard.approval_queue_panel_content_contract import (
    build_approval_queue_panel_content_contract,
)
from MAKSIMAR_CORE_LIB.oob_dashboard.audit_timeline_panel_content_contract import (
    build_audit_timeline_panel_content_contract,
)
from MAKSIMAR_CORE_LIB.oob_dashboard.owner_review_package_models import (
    OwnerReviewPackageContract,
    OwnerReviewPackageEntry,
)
from MAKSIMAR_CORE_LIB.oob_dashboard.preview_surface_contract import (
    build_preview_surface_contract,
)


def build_owner_review_package_contract() -> OwnerReviewPackageContract:
    """Build canonical owner review package contract."""
    preview_surface_contract = build_preview_surface_contract()
    action_queue_contract = build_action_queue_panel_content_contract()
    approval_queue_contract = build_approval_queue_panel_content_contract()
    audit_timeline_contract = build_audit_timeline_panel_content_contract()

    preview_surface_by_panel = {
        entry.panel_id: entry for entry in preview_surface_contract.entries
    }

    approval_by_intent = {
        entry.operator_intent_id: entry for entry in approval_queue_contract.entries
    }

    audit_by_intent = {
        entry.operator_intent_id: entry for entry in audit_timeline_contract.entries
    }

    panel_id_by_intent = {
        "operator_intent_001": "action_queue",
        "operator_intent_002": "action_queue",
        "operator_intent_003": "approval_queue",
    }

    entries = tuple(
        OwnerReviewPackageEntry(
            owner_review_package_id=f"owner_review_package_{index:03d}",
            operator_intent_id=entry.operator_intent_id,
            panel_id=panel_id_by_intent[entry.operator_intent_id],
            workspace_id=preview_surface_by_panel[
                panel_id_by_intent[entry.operator_intent_id]
            ].workspace_id,
            owner_review_package_state="owner_review_package_ready",
            owner_review_package_class=(
                "approval_bound_review_package"
                if entry.approval_required
                else "read_only_review_package"
            ),
            owner_review_evidence_mode=(
                "preview_approval_and_audit_evidence"
                if entry.approval_required
                else "preview_and_audit_evidence"
            ),
            approval_required=entry.approval_required,
            handoff_ready=entry.handoff_ready,
            audit_visible=audit_by_intent[entry.operator_intent_id].audit_visible,
            operator_visible=entry.operator_visible,
            trace_id=entry.trace_id,
            description=(
                "Canonical owner review package entry for "
                f"{entry.operator_intent_id}."
            ),
        )
        for index, entry in enumerate(action_queue_contract.entries, start=1)
    )

    if "operator_intent_003" not in approval_by_intent:
        raise ValueError(
            "approval_queue_contract must expose operator_intent_003 for canonical owner review package."
        )

    return OwnerReviewPackageContract(
        contract_id="owner_review_package_contract_001",
        total_entries=len(entries),
        read_only_review_entries=sum(
            1
            for entry in entries
            if entry.owner_review_package_class == "read_only_review_package"
        ),
        approval_bound_review_entries=sum(
            1
            for entry in entries
            if entry.owner_review_package_class == "approval_bound_review_package"
        ),
        audit_visible_entries=sum(1 for entry in entries if entry.audit_visible),
        operator_visible_entries=sum(
            1 for entry in entries if entry.operator_visible
        ),
        entries=entries,
    )

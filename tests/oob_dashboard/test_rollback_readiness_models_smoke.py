from __future__ import annotations

import pytest

from MAKSIMAR_CORE_LIB.oob_dashboard.rollback_readiness_models import (
    RollbackReadinessContract,
    RollbackReadinessEntry,
)


def test_rollback_readiness_entry_builds() -> None:
    """Rollback readiness entry should build successfully."""
    entry = RollbackReadinessEntry(
        rollback_readiness_id="rollback_readiness_001",
        operator_intent_id="operator_intent_001",
        panel_id="action_queue",
        workspace_id="workspace_operator_main",
        rollback_readiness_state="rollback_readiness_ready",
        rollback_readiness_class="read_only_rollback_readiness",
        rollback_readiness_mode="preview_review_simulation_replay_sandbox_risk_rollback_readiness",
        approval_required=False,
        handoff_ready=True,
        rollback_visible=True,
        operator_visible=True,
        trace_id="trace_operator_intent_001",
        description="Canonical rollback readiness entry.",
    )

    assert entry.rollback_readiness_id == "rollback_readiness_001"
    assert entry.rollback_readiness_state == "rollback_readiness_ready"
    assert entry.rollback_readiness_class == "read_only_rollback_readiness"


def test_rollback_readiness_entry_rejects_non_rollback_visible() -> None:
    """Rollback readiness entry must remain rollback-visible."""
    with pytest.raises(
        ValueError,
        match="rollback_visible must remain true for canonical rollback readiness entries.",
    ):
        RollbackReadinessEntry(
            rollback_readiness_id="rollback_readiness_invalid",
            operator_intent_id="operator_intent_001",
            panel_id="action_queue",
            workspace_id="workspace_operator_main",
            rollback_readiness_state="rollback_readiness_ready",
            rollback_readiness_class="read_only_rollback_readiness",
            rollback_readiness_mode="preview_review_simulation_replay_sandbox_risk_rollback_readiness",
            approval_required=False,
            handoff_ready=True,
            rollback_visible=False,
            operator_visible=True,
            trace_id="trace_operator_intent_001",
            description="Invalid rollback readiness entry.",
        )


def test_rollback_readiness_contract_builds() -> None:
    """Rollback readiness contract should build successfully."""
    entries = (
        RollbackReadinessEntry(
            rollback_readiness_id="rollback_readiness_001",
            operator_intent_id="operator_intent_001",
            panel_id="action_queue",
            workspace_id="workspace_operator_main",
            rollback_readiness_state="rollback_readiness_ready",
            rollback_readiness_class="read_only_rollback_readiness",
            rollback_readiness_mode="preview_review_simulation_replay_sandbox_risk_rollback_readiness",
            approval_required=False,
            handoff_ready=True,
            rollback_visible=True,
            operator_visible=True,
            trace_id="trace_operator_intent_001",
            description="Read-only rollback readiness entry.",
        ),
        RollbackReadinessEntry(
            rollback_readiness_id="rollback_readiness_002",
            operator_intent_id="operator_intent_003",
            panel_id="approval_queue",
            workspace_id="workspace_operator_main",
            rollback_readiness_state="rollback_readiness_ready",
            rollback_readiness_class="approval_bound_rollback_readiness",
            rollback_readiness_mode="preview_review_approval_simulation_replay_sandbox_risk_rollback_readiness",
            approval_required=True,
            handoff_ready=True,
            rollback_visible=True,
            operator_visible=True,
            trace_id="trace_operator_intent_003",
            description="Approval-bound rollback readiness entry.",
        ),
    )

    contract = RollbackReadinessContract(
        contract_id="rollback_readiness_contract_001",
        total_entries=2,
        read_only_rollback_entries=1,
        approval_bound_rollback_entries=1,
        rollback_visible_entries=2,
        operator_visible_entries=2,
        entries=entries,
    )

    assert contract.total_entries == 2
    assert contract.read_only_rollback_entries == 1
    assert contract.approval_bound_rollback_entries == 1

from __future__ import annotations

import pytest

from MAKSIMAR_CORE_LIB.oob_dashboard.risk_summary_models import (
    RiskSummaryContract,
    RiskSummaryEntry,
)


def test_risk_summary_entry_builds() -> None:
    """Risk summary entry should build successfully."""
    entry = RiskSummaryEntry(
        risk_summary_id="risk_summary_001",
        operator_intent_id="operator_intent_001",
        panel_id="action_queue",
        workspace_id="workspace_operator_main",
        risk_summary_state="risk_summary_ready",
        risk_summary_class="read_only_risk_summary",
        risk_summary_mode="preview_review_simulation_replay_sandbox_risk_summary",
        approval_required=False,
        handoff_ready=True,
        risk_visible=True,
        operator_visible=True,
        trace_id="trace_operator_intent_001",
        description="Canonical risk summary entry.",
    )

    assert entry.risk_summary_id == "risk_summary_001"
    assert entry.risk_summary_state == "risk_summary_ready"
    assert entry.risk_summary_class == "read_only_risk_summary"


def test_risk_summary_entry_rejects_non_risk_visible() -> None:
    """Risk summary entry must remain risk-visible."""
    with pytest.raises(
        ValueError,
        match="risk_visible must remain true for canonical risk summaries.",
    ):
        RiskSummaryEntry(
            risk_summary_id="risk_summary_invalid",
            operator_intent_id="operator_intent_001",
            panel_id="action_queue",
            workspace_id="workspace_operator_main",
            risk_summary_state="risk_summary_ready",
            risk_summary_class="read_only_risk_summary",
            risk_summary_mode="preview_review_simulation_replay_sandbox_risk_summary",
            approval_required=False,
            handoff_ready=True,
            risk_visible=False,
            operator_visible=True,
            trace_id="trace_operator_intent_001",
            description="Invalid risk summary entry.",
        )


def test_risk_summary_contract_builds() -> None:
    """Risk summary contract should build successfully."""
    entries = (
        RiskSummaryEntry(
            risk_summary_id="risk_summary_001",
            operator_intent_id="operator_intent_001",
            panel_id="action_queue",
            workspace_id="workspace_operator_main",
            risk_summary_state="risk_summary_ready",
            risk_summary_class="read_only_risk_summary",
            risk_summary_mode="preview_review_simulation_replay_sandbox_risk_summary",
            approval_required=False,
            handoff_ready=True,
            risk_visible=True,
            operator_visible=True,
            trace_id="trace_operator_intent_001",
            description="Read-only risk summary entry.",
        ),
        RiskSummaryEntry(
            risk_summary_id="risk_summary_002",
            operator_intent_id="operator_intent_003",
            panel_id="approval_queue",
            workspace_id="workspace_operator_main",
            risk_summary_state="risk_summary_ready",
            risk_summary_class="approval_bound_risk_summary",
            risk_summary_mode="preview_review_approval_simulation_replay_sandbox_risk_summary",
            approval_required=True,
            handoff_ready=True,
            risk_visible=True,
            operator_visible=True,
            trace_id="trace_operator_intent_003",
            description="Approval-bound risk summary entry.",
        ),
    )

    contract = RiskSummaryContract(
        contract_id="risk_summary_contract_001",
        total_entries=2,
        read_only_risk_entries=1,
        approval_bound_risk_entries=1,
        risk_visible_entries=2,
        operator_visible_entries=2,
        entries=entries,
    )

    assert contract.total_entries == 2
    assert contract.read_only_risk_entries == 1
    assert contract.approval_bound_risk_entries == 1

from __future__ import annotations

from MAKSIMAR_CORE_LIB.oob_dashboard.risk_summary_models import (
    RiskSummaryContract,
    RiskSummaryEntry,
)
from MAKSIMAR_CORE_LIB.oob_dashboard.sandbox_route_contract import (
    build_sandbox_route_contract,
)


def build_risk_summary_contract() -> RiskSummaryContract:
    """Build canonical risk summary contract."""
    sandbox_route_contract = build_sandbox_route_contract()

    entries = tuple(
        RiskSummaryEntry(
            risk_summary_id=f"risk_summary_{index:03d}",
            operator_intent_id=entry.operator_intent_id,
            panel_id=entry.panel_id,
            workspace_id=entry.workspace_id,
            risk_summary_state="risk_summary_ready",
            risk_summary_class=(
                "approval_bound_risk_summary"
                if entry.approval_required
                else "read_only_risk_summary"
            ),
            risk_summary_mode=(
                "preview_review_approval_simulation_replay_sandbox_risk_summary"
                if entry.approval_required
                else "preview_review_simulation_replay_sandbox_risk_summary"
            ),
            approval_required=entry.approval_required,
            handoff_ready=entry.handoff_ready,
            risk_visible=entry.sandbox_visible,
            operator_visible=entry.operator_visible,
            trace_id=entry.trace_id,
            description=(
                "Canonical risk summary entry for "
                f"{entry.operator_intent_id}."
            ),
        )
        for index, entry in enumerate(sandbox_route_contract.entries, start=1)
    )

    return RiskSummaryContract(
        contract_id="risk_summary_contract_001",
        total_entries=len(entries),
        read_only_risk_entries=sum(
            1
            for entry in entries
            if entry.risk_summary_class == "read_only_risk_summary"
        ),
        approval_bound_risk_entries=sum(
            1
            for entry in entries
            if entry.risk_summary_class == "approval_bound_risk_summary"
        ),
        risk_visible_entries=sum(1 for entry in entries if entry.risk_visible),
        operator_visible_entries=sum(
            1 for entry in entries if entry.operator_visible
        ),
        entries=entries,
    )

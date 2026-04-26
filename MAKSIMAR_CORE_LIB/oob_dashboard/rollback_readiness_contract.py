from __future__ import annotations

from MAKSIMAR_CORE_LIB.oob_dashboard.rollback_readiness_models import (
    RollbackReadinessContract,
    RollbackReadinessEntry,
)
from MAKSIMAR_CORE_LIB.oob_dashboard.risk_summary_contract import (
    build_risk_summary_contract,
)


def build_rollback_readiness_contract() -> RollbackReadinessContract:
    """Build canonical rollback readiness contract."""
    risk_summary_contract = build_risk_summary_contract()

    entries = tuple(
        RollbackReadinessEntry(
            rollback_readiness_id=f"rollback_readiness_{index:03d}",
            operator_intent_id=entry.operator_intent_id,
            panel_id=entry.panel_id,
            workspace_id=entry.workspace_id,
            rollback_readiness_state="rollback_readiness_ready",
            rollback_readiness_class=(
                "approval_bound_rollback_readiness"
                if entry.approval_required
                else "read_only_rollback_readiness"
            ),
            rollback_readiness_mode=(
                "preview_review_approval_simulation_replay_sandbox_risk_rollback_readiness"
                if entry.approval_required
                else "preview_review_simulation_replay_sandbox_risk_rollback_readiness"
            ),
            approval_required=entry.approval_required,
            handoff_ready=entry.handoff_ready,
            rollback_visible=entry.risk_visible,
            operator_visible=entry.operator_visible,
            trace_id=entry.trace_id,
            description=(
                "Canonical rollback readiness entry for "
                f"{entry.operator_intent_id}."
            ),
        )
        for index, entry in enumerate(risk_summary_contract.entries, start=1)
    )

    return RollbackReadinessContract(
        contract_id="rollback_readiness_contract_001",
        total_entries=len(entries),
        read_only_rollback_entries=sum(
            1
            for entry in entries
            if entry.rollback_readiness_class == "read_only_rollback_readiness"
        ),
        approval_bound_rollback_entries=sum(
            1
            for entry in entries
            if entry.rollback_readiness_class == "approval_bound_rollback_readiness"
        ),
        rollback_visible_entries=sum(
            1 for entry in entries if entry.rollback_visible
        ),
        operator_visible_entries=sum(
            1 for entry in entries if entry.operator_visible
        ),
        entries=entries,
    )

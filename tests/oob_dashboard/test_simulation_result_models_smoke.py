from __future__ import annotations

import pytest

from MAKSIMAR_CORE_LIB.oob_dashboard.simulation_result_models import (
    SimulationResultContract,
    SimulationResultEntry,
)


def test_simulation_result_entry_builds() -> None:
    """Simulation result entry should build successfully."""
    entry = SimulationResultEntry(
        simulation_result_id="simulation_result_001",
        operator_intent_id="operator_intent_001",
        panel_id="action_queue",
        workspace_id="workspace_operator_main",
        simulation_result_state="simulation_result_ready",
        simulation_result_class="read_only_simulation_result",
        simulation_evidence_mode="preview_review_simulation_evidence",
        approval_required=False,
        handoff_ready=True,
        review_visible=True,
        operator_visible=True,
        trace_id="trace_operator_intent_001",
        description="Canonical simulation result entry.",
    )

    assert entry.simulation_result_id == "simulation_result_001"
    assert entry.simulation_result_state == "simulation_result_ready"
    assert entry.simulation_result_class == "read_only_simulation_result"


def test_simulation_result_entry_rejects_non_review_visible() -> None:
    """Simulation result entry must remain review-visible."""
    with pytest.raises(
        ValueError,
        match="review_visible must remain true for canonical simulation results.",
    ):
        SimulationResultEntry(
            simulation_result_id="simulation_result_invalid",
            operator_intent_id="operator_intent_001",
            panel_id="action_queue",
            workspace_id="workspace_operator_main",
            simulation_result_state="simulation_result_ready",
            simulation_result_class="read_only_simulation_result",
            simulation_evidence_mode="preview_review_simulation_evidence",
            approval_required=False,
            handoff_ready=True,
            review_visible=False,
            operator_visible=True,
            trace_id="trace_operator_intent_001",
            description="Invalid simulation result entry.",
        )


def test_simulation_result_contract_builds() -> None:
    """Simulation result contract should build successfully."""
    entries = (
        SimulationResultEntry(
            simulation_result_id="simulation_result_001",
            operator_intent_id="operator_intent_001",
            panel_id="action_queue",
            workspace_id="workspace_operator_main",
            simulation_result_state="simulation_result_ready",
            simulation_result_class="read_only_simulation_result",
            simulation_evidence_mode="preview_review_simulation_evidence",
            approval_required=False,
            handoff_ready=True,
            review_visible=True,
            operator_visible=True,
            trace_id="trace_operator_intent_001",
            description="Read-only simulation result entry.",
        ),
        SimulationResultEntry(
            simulation_result_id="simulation_result_002",
            operator_intent_id="operator_intent_003",
            panel_id="approval_queue",
            workspace_id="workspace_operator_main",
            simulation_result_state="simulation_result_ready",
            simulation_result_class="approval_bound_simulation_result",
            simulation_evidence_mode="preview_review_approval_simulation_evidence",
            approval_required=True,
            handoff_ready=True,
            review_visible=True,
            operator_visible=True,
            trace_id="trace_operator_intent_003",
            description="Approval-bound simulation result entry.",
        ),
    )

    contract = SimulationResultContract(
        contract_id="simulation_result_contract_001",
        total_entries=2,
        read_only_simulation_entries=1,
        approval_bound_simulation_entries=1,
        review_visible_entries=2,
        operator_visible_entries=2,
        entries=entries,
    )

    assert contract.total_entries == 2
    assert contract.read_only_simulation_entries == 1
    assert contract.approval_bound_simulation_entries == 1

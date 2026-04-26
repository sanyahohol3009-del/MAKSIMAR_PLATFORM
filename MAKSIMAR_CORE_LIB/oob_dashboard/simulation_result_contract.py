from __future__ import annotations

from MAKSIMAR_CORE_LIB.oob_dashboard.owner_review_package_contract import (
    build_owner_review_package_contract,
)
from MAKSIMAR_CORE_LIB.oob_dashboard.preview_surface_contract import (
    build_preview_surface_contract,
)
from MAKSIMAR_CORE_LIB.oob_dashboard.simulation_result_models import (
    SimulationResultContract,
    SimulationResultEntry,
)


def build_simulation_result_contract() -> SimulationResultContract:
    """Build canonical simulation result contract."""
    preview_surface_contract = build_preview_surface_contract()
    owner_review_package_contract = build_owner_review_package_contract()

    preview_surface_by_panel = {
        entry.panel_id: entry for entry in preview_surface_contract.entries
    }

    entries = tuple(
        SimulationResultEntry(
            simulation_result_id=f"simulation_result_{index:03d}",
            operator_intent_id=entry.operator_intent_id,
            panel_id=entry.panel_id,
            workspace_id=preview_surface_by_panel[entry.panel_id].workspace_id,
            simulation_result_state="simulation_result_ready",
            simulation_result_class=(
                "approval_bound_simulation_result"
                if entry.approval_required
                else "read_only_simulation_result"
            ),
            simulation_evidence_mode=(
                "preview_review_approval_simulation_evidence"
                if entry.approval_required
                else "preview_review_simulation_evidence"
            ),
            approval_required=entry.approval_required,
            handoff_ready=entry.handoff_ready,
            review_visible=entry.audit_visible,
            operator_visible=entry.operator_visible,
            trace_id=entry.trace_id,
            description=(
                "Canonical simulation result entry for "
                f"{entry.operator_intent_id}."
            ),
        )
        for index, entry in enumerate(owner_review_package_contract.entries, start=1)
    )

    return SimulationResultContract(
        contract_id="simulation_result_contract_001",
        total_entries=len(entries),
        read_only_simulation_entries=sum(
            1
            for entry in entries
            if entry.simulation_result_class == "read_only_simulation_result"
        ),
        approval_bound_simulation_entries=sum(
            1
            for entry in entries
            if entry.simulation_result_class == "approval_bound_simulation_result"
        ),
        review_visible_entries=sum(1 for entry in entries if entry.review_visible),
        operator_visible_entries=sum(
            1 for entry in entries if entry.operator_visible
        ),
        entries=entries,
    )

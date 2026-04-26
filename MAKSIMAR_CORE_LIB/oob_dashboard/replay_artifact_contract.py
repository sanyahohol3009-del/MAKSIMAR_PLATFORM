from __future__ import annotations

from MAKSIMAR_CORE_LIB.oob_dashboard.preview_surface_contract import (
    build_preview_surface_contract,
)
from MAKSIMAR_CORE_LIB.oob_dashboard.replay_artifact_models import (
    ReplayArtifactContract,
    ReplayArtifactEntry,
)
from MAKSIMAR_CORE_LIB.oob_dashboard.simulation_result_contract import (
    build_simulation_result_contract,
)


def build_replay_artifact_contract() -> ReplayArtifactContract:
    """Build canonical replay artifact contract."""
    preview_surface_contract = build_preview_surface_contract()
    simulation_result_contract = build_simulation_result_contract()

    preview_surface_by_panel = {
        entry.panel_id: entry for entry in preview_surface_contract.entries
    }

    entries = tuple(
        ReplayArtifactEntry(
            replay_artifact_id=f"replay_artifact_{index:03d}",
            operator_intent_id=entry.operator_intent_id,
            panel_id=entry.panel_id,
            workspace_id=preview_surface_by_panel[entry.panel_id].workspace_id,
            replay_artifact_state="replay_artifact_ready",
            replay_artifact_class=(
                "approval_bound_replay_artifact"
                if entry.approval_required
                else "read_only_replay_artifact"
            ),
            replay_evidence_mode=(
                "preview_review_approval_simulation_replay_evidence"
                if entry.approval_required
                else "preview_review_simulation_replay_evidence"
            ),
            approval_required=entry.approval_required,
            handoff_ready=entry.handoff_ready,
            replay_visible=entry.review_visible,
            operator_visible=entry.operator_visible,
            trace_id=entry.trace_id,
            description=(
                "Canonical replay artifact entry for "
                f"{entry.operator_intent_id}."
            ),
        )
        for index, entry in enumerate(simulation_result_contract.entries, start=1)
    )

    return ReplayArtifactContract(
        contract_id="replay_artifact_contract_001",
        total_entries=len(entries),
        read_only_replay_entries=sum(
            1
            for entry in entries
            if entry.replay_artifact_class == "read_only_replay_artifact"
        ),
        approval_bound_replay_entries=sum(
            1
            for entry in entries
            if entry.replay_artifact_class == "approval_bound_replay_artifact"
        ),
        replay_visible_entries=sum(1 for entry in entries if entry.replay_visible),
        operator_visible_entries=sum(
            1 for entry in entries if entry.operator_visible
        ),
        entries=entries,
    )

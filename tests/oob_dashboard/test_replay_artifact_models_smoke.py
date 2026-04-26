from __future__ import annotations

import pytest

from MAKSIMAR_CORE_LIB.oob_dashboard.replay_artifact_models import (
    ReplayArtifactContract,
    ReplayArtifactEntry,
)


def test_replay_artifact_entry_builds() -> None:
    """Replay artifact entry should build successfully."""
    entry = ReplayArtifactEntry(
        replay_artifact_id="replay_artifact_001",
        operator_intent_id="operator_intent_001",
        panel_id="action_queue",
        workspace_id="workspace_operator_main",
        replay_artifact_state="replay_artifact_ready",
        replay_artifact_class="read_only_replay_artifact",
        replay_evidence_mode="preview_review_simulation_replay_evidence",
        approval_required=False,
        handoff_ready=True,
        replay_visible=True,
        operator_visible=True,
        trace_id="trace_operator_intent_001",
        description="Canonical replay artifact entry.",
    )

    assert entry.replay_artifact_id == "replay_artifact_001"
    assert entry.replay_artifact_state == "replay_artifact_ready"
    assert entry.replay_artifact_class == "read_only_replay_artifact"


def test_replay_artifact_entry_rejects_non_replay_visible() -> None:
    """Replay artifact entry must remain replay-visible."""
    with pytest.raises(
        ValueError,
        match="replay_visible must remain true for canonical replay artifacts.",
    ):
        ReplayArtifactEntry(
            replay_artifact_id="replay_artifact_invalid",
            operator_intent_id="operator_intent_001",
            panel_id="action_queue",
            workspace_id="workspace_operator_main",
            replay_artifact_state="replay_artifact_ready",
            replay_artifact_class="read_only_replay_artifact",
            replay_evidence_mode="preview_review_simulation_replay_evidence",
            approval_required=False,
            handoff_ready=True,
            replay_visible=False,
            operator_visible=True,
            trace_id="trace_operator_intent_001",
            description="Invalid replay artifact entry.",
        )


def test_replay_artifact_contract_builds() -> None:
    """Replay artifact contract should build successfully."""
    entries = (
        ReplayArtifactEntry(
            replay_artifact_id="replay_artifact_001",
            operator_intent_id="operator_intent_001",
            panel_id="action_queue",
            workspace_id="workspace_operator_main",
            replay_artifact_state="replay_artifact_ready",
            replay_artifact_class="read_only_replay_artifact",
            replay_evidence_mode="preview_review_simulation_replay_evidence",
            approval_required=False,
            handoff_ready=True,
            replay_visible=True,
            operator_visible=True,
            trace_id="trace_operator_intent_001",
            description="Read-only replay artifact entry.",
        ),
        ReplayArtifactEntry(
            replay_artifact_id="replay_artifact_002",
            operator_intent_id="operator_intent_003",
            panel_id="approval_queue",
            workspace_id="workspace_operator_main",
            replay_artifact_state="replay_artifact_ready",
            replay_artifact_class="approval_bound_replay_artifact",
            replay_evidence_mode="preview_review_approval_simulation_replay_evidence",
            approval_required=True,
            handoff_ready=True,
            replay_visible=True,
            operator_visible=True,
            trace_id="trace_operator_intent_003",
            description="Approval-bound replay artifact entry.",
        ),
    )

    contract = ReplayArtifactContract(
        contract_id="replay_artifact_contract_001",
        total_entries=2,
        read_only_replay_entries=1,
        approval_bound_replay_entries=1,
        replay_visible_entries=2,
        operator_visible_entries=2,
        entries=entries,
    )

    assert contract.total_entries == 2
    assert contract.read_only_replay_entries == 1
    assert contract.approval_bound_replay_entries == 1

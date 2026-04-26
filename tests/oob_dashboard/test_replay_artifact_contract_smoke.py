from __future__ import annotations

from MAKSIMAR_CORE_LIB.oob_dashboard.replay_artifact_contract import (
    build_replay_artifact_contract,
)


def test_replay_artifact_contract_builds() -> None:
    """Replay artifact contract should build successfully."""
    contract = build_replay_artifact_contract()

    assert contract.contract_id == "replay_artifact_contract_001"
    assert contract.total_entries == 3
    assert contract.read_only_replay_entries == 2
    assert contract.approval_bound_replay_entries == 1
    assert contract.replay_visible_entries == 3
    assert contract.operator_visible_entries == 3


def test_replay_artifact_contract_contains_expected_entries() -> None:
    """Replay artifact contract should contain expected canonical entries."""
    contract = build_replay_artifact_contract()
    entry_map = {entry.operator_intent_id: entry for entry in contract.entries}

    assert (
        entry_map["operator_intent_001"].replay_artifact_class
        == "read_only_replay_artifact"
    )
    assert (
        entry_map["operator_intent_001"].replay_evidence_mode
        == "preview_review_simulation_replay_evidence"
    )
    assert entry_map["operator_intent_001"].panel_id == "action_queue"

    assert (
        entry_map["operator_intent_002"].replay_artifact_class
        == "read_only_replay_artifact"
    )
    assert entry_map["operator_intent_002"].panel_id == "action_queue"

    assert (
        entry_map["operator_intent_003"].replay_artifact_class
        == "approval_bound_replay_artifact"
    )
    assert (
        entry_map["operator_intent_003"].replay_evidence_mode
        == "preview_review_approval_simulation_replay_evidence"
    )
    assert entry_map["operator_intent_003"].panel_id == "approval_queue"

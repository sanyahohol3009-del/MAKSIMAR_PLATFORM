from __future__ import annotations

from MAKSIMAR_SERVER.MEMORY_CONFLICT_RESOLUTION import (
    build_memory_conflict_resolution_contract,
)


def test_memory_conflict_resolution_contract_builds() -> None:
    """Memory conflict resolution contract should build successfully."""
    contract = build_memory_conflict_resolution_contract()

    assert contract.total_entries == 2
    assert contract.promote_new_version_entries == 1
    assert contract.keep_existing_entries == 1
    assert contract.approval_required_entries == 2


def test_memory_conflict_resolution_contract_contains_expected_promote_case() -> None:
    """Memory conflict resolution should expose expected version-promotion case."""
    contract = build_memory_conflict_resolution_contract()
    entry = contract.entries[0]

    assert entry.module_slug == "project_architecture"
    assert entry.memory_tier_id == "memory_project_architecture"
    assert entry.conflict_case_id == "conflict_architecture_decision_002"
    assert entry.fact_class == "architecture_decision"
    assert entry.resolution_strategy == "promote_new_version"
    assert entry.resolved_record_id == "memrec_architecture_decision_002"
    assert entry.archived_record_id == "archive_architecture_decision_001"
    assert entry.version_incremented is True


def test_memory_conflict_resolution_contract_contains_expected_keep_case() -> None:
    """Memory conflict resolution should expose expected keep-existing case."""
    contract = build_memory_conflict_resolution_contract()
    entry = contract.entries[1]

    assert entry.module_slug == "project_architecture"
    assert entry.memory_tier_id == "memory_project_architecture"
    assert entry.conflict_case_id == "conflict_architecture_decision_003"
    assert entry.fact_class == "architecture_decision"
    assert entry.resolution_strategy == "keep_existing_record"
    assert entry.resolved_record_id == "memrec_architecture_decision_002"
    assert entry.archived_record_id == "archive_architecture_decision_003"
    assert entry.version_incremented is False


def test_memory_conflict_resolution_contract_preserves_proposal_and_approval_fields() -> None:
    """Memory conflict resolution should preserve proposal and approval metadata."""
    contract = build_memory_conflict_resolution_contract()

    first = contract.entries[0]
    second = contract.entries[1]

    assert first.proposal_generated is True
    assert first.approval_required is True
    assert first.approval_granted is True
    assert first.conflict_marker_id == "conflictmark_architecture_decision_002"

    assert second.proposal_generated is True
    assert second.approval_required is True
    assert second.approval_granted is True
    assert second.conflict_marker_id == "conflictmark_architecture_decision_003"

from __future__ import annotations

from MAKSIMAR_CORE_LIB.memory_policy import (
    build_memory_classification_policy_contract,
)


def test_memory_classification_policy_contract_builds() -> None:
    """Memory classification policy contract should build successfully."""
    contract = build_memory_classification_policy_contract()

    assert contract.total_entries == 1
    assert contract.active_entries == 1
    assert contract.foundational_entries == 1
    assert contract.approval_required_entries == 1


def test_memory_classification_policy_contract_contains_expected_entry() -> None:
    """Memory classification policy should expose expected foundational tier."""
    contract = build_memory_classification_policy_contract()
    entry = contract.entries[0]

    assert entry.module_slug == "project_architecture"
    assert entry.memory_tier_id == "memory_project_architecture"
    assert entry.retention_class == "foundational"
    assert entry.approval_mode == "mandatory_human_approval"
    assert entry.summarization_mode == "summary_required"
    assert entry.deduplication_mode == "deduplicate_before_write"
    assert entry.conflict_mode == "conflict_check_required"


def test_memory_classification_policy_contract_preserves_multilingual_and_provenance_rules() -> None:
    """Memory classification policy should preserve metadata requirements."""
    contract = build_memory_classification_policy_contract()
    entry = contract.entries[0]

    assert entry.accepted_fact_classes == (
        "architecture_decision",
        "platform_invariant",
        "roadmap_checkpoint",
    )
    assert entry.language_policy == "language_metadata_required"
    assert entry.script_policy == "script_metadata_required"
    assert entry.provenance_policy == "provenance_required"
    assert entry.evidence_required is True
    assert entry.active is True


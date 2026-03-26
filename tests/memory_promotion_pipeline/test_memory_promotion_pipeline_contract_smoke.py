from __future__ import annotations

from MAKSIMAR_SERVER.MEMORY_PROMOTION_PIPELINE import (
    build_memory_promotion_pipeline_contract,
)


def test_memory_promotion_pipeline_contract_builds() -> None:
    """Memory promotion pipeline contract should build successfully."""
    contract = build_memory_promotion_pipeline_contract()

    assert contract.total_entries == 2
    assert contract.promoted_entries == 1
    assert contract.archived_entries == 1
    assert contract.evidence_bound_entries == 2


def test_memory_promotion_pipeline_contract_contains_expected_promoted_entry() -> None:
    """Memory promotion pipeline should expose expected promoted entry."""
    contract = build_memory_promotion_pipeline_contract()
    entry = contract.entries[0]

    assert entry.module_slug == "project_architecture"
    assert entry.memory_tier_id == "memory_project_architecture"
    assert entry.input_event_id == "event_architecture_decision_001"
    assert entry.fact_class == "architecture_decision"
    assert entry.final_disposition == "promoted"
    assert entry.promoted_record_id == "memrec_architecture_decision_001"
    assert entry.archived_record_id == ""


def test_memory_promotion_pipeline_contract_contains_expected_archived_entry() -> None:
    """Memory promotion pipeline should expose expected archived duplicate entry."""
    contract = build_memory_promotion_pipeline_contract()
    entry = contract.entries[1]

    assert entry.module_slug == "project_architecture"
    assert entry.memory_tier_id == "memory_project_architecture"
    assert entry.input_event_id == "event_roadmap_checkpoint_001"
    assert entry.fact_class == "roadmap_checkpoint"
    assert entry.final_disposition == "archived"
    assert entry.archive_reason == "duplicate_candidate"
    assert entry.promoted_record_id == ""
    assert entry.archived_record_id == "archive_roadmap_checkpoint_001"
    assert entry.deduplication_passed is False
    assert entry.conflict_check_performed is False


def test_memory_promotion_pipeline_contract_preserves_multilingual_and_provenance_fields() -> None:
    """Memory promotion pipeline should preserve language, script, and provenance metadata."""
    contract = build_memory_promotion_pipeline_contract()

    first = contract.entries[0]
    second = contract.entries[1]

    assert first.language_code == "ru"
    assert first.script_name == "Cyrillic"
    assert first.provenance_ref == "prov_architecture_decision_001"

    assert second.language_code == "en"
    assert second.script_name == "Latin"
    assert second.provenance_ref == "prov_roadmap_checkpoint_001"
